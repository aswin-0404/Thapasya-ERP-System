from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EnquiryCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str

class Enquiry(EnquiryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True