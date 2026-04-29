from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class NotificationTarget(str, enum.Enum):
    ALL = "all"
    STAFF = "staff"
    STUDENTS = "students"
    COURSE = "course"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    # Targeting Logic
    target_type = Column(String, default=NotificationTarget.ALL) # ALL, STAFF, STUDENTS, COURSE
    target_id = Column(Integer, nullable=True) # Used if target_type is 'COURSE' (stores course_id)
    
    sender_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User")

class UserDeviceToken(Base):
    """Stores FCM tokens for mobile push notifications"""
    __tablename__ = "user_device_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False) # The FCM token from the phone
    device_type = Column(String, nullable=True) # e.g., "android" or "ios"
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="device_tokens")