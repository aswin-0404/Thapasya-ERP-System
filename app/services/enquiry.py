from sqlalchemy.orm import Session
from app.repositories.enquiries import EnquiryRepository
from app.schemas.enquiries import EnquiryCreate

class EnquiryService:
    def __init__(self, db: Session):
        self.repository = EnquiryRepository(db)

    def create_enquiry(self, enquiry_data: EnquiryCreate):
        # Business Logic goes here (e.g., sending an email notification)
        return self.repository.create(enquiry_data)

    def get_all_enquiries(self):
        return self.repository.get_all()