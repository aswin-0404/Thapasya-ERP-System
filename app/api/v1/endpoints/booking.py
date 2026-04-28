from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db 
from app.models.booking import ProgramBooking
from app.models.course import Course
from app.schemas.booking import BookingCreate, BookingResponse
from app.core.dependencies import get_current_admin

router = APIRouter()

@router.post("/", response_model=BookingResponse)
def create_program_booking(
    *, 
    db: Session = Depends(get_db), 
    booking_in: BookingCreate
):
    """
    Create a new booking that can include multiple course IDs.
    """
    # 1. Fetch all Course objects that match the IDs in the request
    selected_courses = db.query(Course).filter(Course.id.in_(booking_in.course_ids)).all()
    
    # Validation: Make sure all IDs sent by the frontend actually exist
    if len(selected_courses) != len(booking_in.course_ids):
        raise HTTPException(
            status_code=400, 
            detail="One or more Course IDs are invalid or do not exist."
        )

    # 2. Create the booking object (excluding the list of IDs from the main model)
    booking_data = booking_in.dict(exclude={"course_ids"})
    db_obj = ProgramBooking(**booking_data)
    
    # 3. Attach the actual Course objects to the relationship
    db_obj.courses = selected_courses
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin = Depends(get_current_admin)
):
    """
    Retrieve all bookings. Each booking will include its list of associated courses.
    """
    bookings = db.query(ProgramBooking).offset(skip).limit(limit).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking_by_id(
    booking_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """
    Get details of a specific booking by its ID.
    """
    booking = db.query(ProgramBooking).filter(ProgramBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking