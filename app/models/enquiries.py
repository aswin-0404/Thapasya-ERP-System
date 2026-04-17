from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from datetime import datetime
from app.db.base_class import Base

class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key = True, index = True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    status = Column(String, default="Pending") # Pending, Converted, Rejected
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    admin_notes = Column(String, nullable=True) # For keeping track of enquiries