from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

# 🔗 The Link Table (Many-to-Many)
booking_courses = Table(
    "booking_courses",
    Base.metadata,
    Column("booking_id", Integer, ForeignKey("program_bookings.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)

class ProgramBooking(Base):
    __tablename__ = "program_bookings"

    id = Column(Integer, primary_key=True, index=True)
    courses = relationship("Course", secondary=booking_courses)
    
    place = Column(String, nullable=False)
    event_date_time = Column(DateTime, nullable=False)
    duration_hours = Column(Float, nullable=False)
    people_count = Column(Integer, nullable=False)
    
    client_name = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    
    budget_offered = Column(Numeric(10, 2), nullable=True)
    description = Column(Text, nullable=True) 
    
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)