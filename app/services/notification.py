from sqlalchemy.orm import Session
from app.models.notification import Notification, UserDeviceToken, NotificationTarget
from app.models.user import User
from app.schemas.notification import NotificationCreate, DeviceTokenCreate
from app.core.push_notifications import send_push_notification
from app.core.websocket import manager

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    async def register_device(self, user_id: int, device_in: DeviceTokenCreate):
        """Register or update a mobile device token"""
        db_token = self.db.query(UserDeviceToken).filter(
            UserDeviceToken.token == device_in.token
        ).first()

        if db_token:
            db_token.user_id = user_id
            db_token.device_type = device_in.device_type
        else:
            db_token = UserDeviceToken(
                user_id=user_id,
                token=device_in.token,
                device_type=device_in.device_type
            )
            self.db.add(db_token)
        
        self.db.commit()
        self.db.refresh(db_token)
        return db_token

    async def create_broadcast(self, sender_id: int, notification_in: NotificationCreate):
        """To save, filter recipients, and send Push/Web notifications"""
        
        # Save to Database (History)
        db_notification = Notification(
            title=notification_in.title,
            content=notification_in.content,
            target_type=notification_in.target_type,
            target_id=notification_in.target_id,
            sender_id=sender_id
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)

        # Get target tokens (Excluding the Principal/Sender)
        tokens = self.get_target_tokens(
            notification_in.target_type, 
            notification_in.target_id,
            exclude_user_id=sender_id
        )

        # Fire Push Notification (to Mobile Devices)
        if tokens:
            send_push_notification(
                tokens=tokens,
                title=notification_in.title,
                body=notification_in.content
            )

        # Fire WebSocket Broadcast (to Web Users)
        await manager.broadcast({
            "event": "NEW_ANNOUNCEMENT",
            "data": {
                "id": db_notification.id,
                "title": db_notification.title,
                "content": db_notification.content,
                "created_at": str(db_notification.created_at)
            }
        })

        return db_notification

    def get_target_tokens(self, target_type: str, target_id: int = None, exclude_user_id: int = None):
        query = self.db.query(UserDeviceToken.token).join(User)

        if target_type == "students":
            query = query.filter(User.role_id == 2)
        
        elif target_type == "staff":
            query = query.filter(User.role_id == 3)
            
        elif target_type == "course" and target_id:
            from app.models.student import Student
            from app.models.student_course import StudentCourse
            
            query = query.join(Student, Student.user_id == User.id)\
                        .join(StudentCourse, StudentCourse.student_id == Student.id)\
                        .filter(StudentCourse.course_id == target_id)

        if exclude_user_id:
            query = query.filter(UserDeviceToken.user_id != exclude_user_id)

        return [t.token for t in query.all()]