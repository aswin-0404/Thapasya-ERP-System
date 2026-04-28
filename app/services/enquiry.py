from sqlalchemy.orm import Session
from app.repositories.enquiries import EnquiryRepository
from app.schemas.enquiries import EnquiryCreate, EnquiryUpdate
from app.core.websocket import manager # Import the manager
import asyncio


class EnquiryService:
    def __init__(self, db: Session):
        self.repository = EnquiryRepository(db)

    async def create_enquiry(self, enquiry_data: EnquiryCreate):
        # 1. Save to Database
        new_enquiry = self.repository.create(enquiry_data)
        
        # 2. Prepare the data for the live dashboard
        live_data = {
            "event": "NEW_ENQUIRY",
            "data": {
                "id": new_enquiry.id,
                "full_name": new_enquiry.full_name,
                "message": new_enquiry.message,
                "created_at": new_enquiry.created_at.isoformat()
            }
        }
        
        # 3. Broadcast to the Admin Dashboard
        await manager.broadcast(live_data)
        
        return new_enquiry

    def get_all_enquiries(self):
        return self.repository.get_all()

    def update_enquiry(self, enquiry_id: int, enquiry_in: EnquiryUpdate):
        # exclude_unset=True ensures we don't overwrite data with nulls
        update_data = enquiry_in.model_dump(exclude_unset=True) 
        return self.repository.update(enquiry_id, update_data)