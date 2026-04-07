from sqlalchemy.orm import Session
from app.repositories.booking import booking_repo
from app.schemas.booking import BookingCreate

class BookingService:
    def create_booking(self, db: Session, *, booking_in: BookingCreate):
        return booking_repo.create(db, obj_in=booking_in)

booking_service = BookingService()