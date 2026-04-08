from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class BookingBase(BaseModel):
    course_ids: List[int] 
    place: str
    event_date_time: datetime
    duration_hours: float
    people_count: int
    client_name: str
    contact_phone: str
    budget_offered: Optional[Decimal] = None
    description: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingResponse(BaseModel):
    id: int
    client_name: str
    place: str
    event_date_time: datetime

    courses: List[dict]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True