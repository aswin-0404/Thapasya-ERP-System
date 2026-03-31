from sqlalchemy.orm import Session
from app.models.enquiries import Enquiry
from app.schemas.enquiries import EnquiryCreate

class EnquiryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, inquiry_data: EnquiryCreate):
        db_inquiry = Enquiry(
            full_name=inquiry_data.full_name,
            email=inquiry_data.email,
            phone=inquiry_data.phone,
            message=inquiry_data.message
        )
        
        self.db.add(db_inquiry)
        
        self.db.commit()
        
        self.db.refresh(db_inquiry)
        return db_inquiry

    def get_all(self):
        return self.db.query(Enquiry).all()