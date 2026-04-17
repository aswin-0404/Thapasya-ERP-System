from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.enquiries import Enquiry, EnquiryCreate, EnquiryAdminResponse, EnquiryUpdate # Added new schemas
from app.services.enquiry import EnquiryService

router = APIRouter()

@router.post("/", response_model=Enquiry)
def create_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    service = EnquiryService(db)
    return service.create_enquiry(enquiry)

# Changed response_model to Admin version so you see status/notes
@router.get("/", response_model=List[EnquiryAdminResponse])
def get_enquiries(db: Session = Depends(get_db)):
    service = EnquiryService(db)
    return service.get_all_enquiries()

# New Update Endpoint
router.put("/{enquiry_id}", response_model=EnquiryAdminResponse)
def update_enquiry(
    enquiry_id: int, 
    enquiry_in: EnquiryUpdate, 
    db: Session = Depends(get_db)
):
    service = EnquiryService(db)
    updated_enquiry = service.update_enquiry(enquiry_id, enquiry_in)
    
    if not updated_enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
        
    return updated_enquiry