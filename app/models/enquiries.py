from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from app.db.base_class import Base

class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    message = Column(Text, nullable=False)

    status = Column(String, default="Pending")  # Pending, Converted, Rejected
    is_active = Column(Boolean, default=True)
    admin_notes = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )