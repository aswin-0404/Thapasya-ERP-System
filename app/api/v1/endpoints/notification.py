from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from typing import List
from app.core.websocket import manager

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.schemas.notification import NotificationCreate,  NotificationResponse,  DeviceTokenCreate,  DeviceTokenResponse
from app.services.notification import NotificationService

router = APIRouter()

@router.post("/register-device", response_model=DeviceTokenResponse)
async def register_device(
    device_in: DeviceTokenCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = NotificationService(db)
    try:
        return await service.register_device(current_user.id, device_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not register device: {str(e)}"
        )

@router.post("/broadcast", response_model=NotificationResponse)
async def create_broadcast(
    notification_in: NotificationCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    service = NotificationService(db)
    
    try:
        notification = await service.create_broadcast(
            sender_id=current_admin.id, 
            notification_in=notification_in
        )
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Broadcast failed: {str(e)}"
        )

@router.get("/history", response_model=List[NotificationResponse])
def get_notification_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.models.notification import Notification
    from app.models.student import Student
    from app.models.student_course import StudentCourse

    query = db.query(Notification)

    if current_user.role_id == 1:
        return query.order_by(Notification.created_at.desc()).limit(50).all()

    role_map = {2: "students", 3: "staff"}
    user_role_type = role_map.get(current_user.role_id)

    filters = [
        (Notification.target_type == "all"),
        (Notification.target_type == user_role_type)
    ]

    if current_user.role_id == 2:
        student_courses = db.query(StudentCourse.course_id)\
            .join(Student, Student.id == StudentCourse.student_id)\
            .filter(Student.user_id == current_user.id).all()
        
        course_ids = [c[0] for c in student_courses]
        
        if course_ids:
            filters.append(
                (Notification.target_type == "course") & 
                (Notification.target_id.in_(course_ids))
            )
    from sqlalchemy import or_
    query = query.filter(or_(*filters))

    return query.order_by(Notification.created_at.desc()).limit(50).all()

@router.websocket("/ws")
async def notification_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() 
    except Exception as e:
        print(f"WS Disconnect: {e}")
        manager.disconnect(websocket)