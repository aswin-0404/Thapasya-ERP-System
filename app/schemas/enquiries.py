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

class EnquiryUpdate(BaseModel):
    status: Optional[str] = None
    is_active: Optional[bool] = None
    admin_notes: Optional[str] = None
    
class EnquiryAdminResponse(Enquiry):
    status: str
    is_active: bool
    admin_notes: Optional[str] = None