from sqlalchemy.orm import Session
from app.repositories.enquiries import EnquiryRepository
from app.schemas.enquiries import EnquiryCreate, EnquiryUpdate

class EnquiryService:
    def __init__(self, db: Session):
        self.repository = EnquiryRepository(db)

    def create_enquiry(self, enquiry_data: EnquiryCreate):
        return self.repository.create(enquiry_data)

    def get_all_enquiries(self):
        return self.repository.get_all()

    def update_enquiry(self, enquiry_id: int, enquiry_in: EnquiryUpdate):
        # exclude_unset=True ensures we don't overwrite data with nulls
        update_data = enquiry_in.model_dump(exclude_unset=True) 
        return self.repository.update(enquiry_id, update_data)