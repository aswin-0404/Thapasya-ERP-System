from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class NotificationTarget(str, Enum):
    ALL = "all"
    STAFF = "staff"
    STUDENTS = "students"
    COURSE = "course"

class NotificationBase(BaseModel):
    title: str
    content: str
    target_type: NotificationTarget = NotificationTarget.ALL
    target_id: Optional[int] = None  # Course ID or Branch ID if needed

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DeviceTokenCreate(BaseModel):
    token: str
    device_type: Optional[str] = "android"  # "android" or "ios"

class DeviceTokenResponse(DeviceTokenCreate):
    id: int
    user_id: int
    last_updated: datetime

    class Config:
        from_attributes = True