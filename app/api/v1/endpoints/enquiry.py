from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.enquiries import Enquiry, EnquiryCreate
from app.services.enquiry import EnquiryService

router = APIRouter()

@router.post("/", response_model=Enquiry)
def create_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    service = EnquiryService(db)
    return service.create_enquiry(enquiry)

@router.get("/", response_model=List[Enquiry])
def get_enquiries(db: Session = Depends(get_db)):
    service = EnquiryService(db)
    return service.get_all_enquiries()