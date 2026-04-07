from sqlalchemy.orm import Session
from app.models.booking import ProgramBooking
from app.schemas.booking import BookingCreate

class BookingRepository:
    def create(self, db: Session, *, obj_in: BookingCreate) -> ProgramBooking:
        db_obj = ProgramBooking(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(ProgramBooking).offset(skip).limit(limit).all()

booking_repo = BookingRepository()