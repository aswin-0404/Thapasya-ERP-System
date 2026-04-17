from sqlalchemy.orm import Session
from app.models.enquiries import Enquiry
from app.schemas.enquiries import EnquiryCreate

class EnquiryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, inquiry_data: EnquiryCreate):
        # Using **inquiry_data.dict() automatically maps all 
        # schema fields to your Model columns
        db_inquiry = Enquiry(**inquiry_data.dict())
        
        self.db.add(db_inquiry)
        self.db.commit()
        self.db.refresh(db_inquiry)
        return db_inquiry

    def get_all(self):
        # Professional tip: You might want to sort by latest first
        return self.db.query(Enquiry).order_by(Enquiry.created_at.desc()).all()

    def update(self, enquiry_id: int, update_data: dict):
        db_obj = self.db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
        if db_obj:
            # This loops through only the fields you sent in the PUT request
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj