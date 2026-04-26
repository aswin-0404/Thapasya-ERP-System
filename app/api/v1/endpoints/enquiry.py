from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Depends
from jose import JWTError
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.enquiries import Enquiry, EnquiryCreate, EnquiryAdminResponse, EnquiryUpdate
from app.services.enquiry import EnquiryService
from app.core.websocket import manager
from app.core.dependencies import get_current_admin

router = APIRouter()

@router.post("/", response_model=Enquiry)
async def create_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    service = EnquiryService(db)
    # Using await here so the WebSocket broadcast inside the service actually happens
    return await service.create_enquiry(enquiry)

# Changed response_model to Admin version to see status/notes
@router.get("/", response_model=List[EnquiryAdminResponse])
def get_enquiries(
    db: Session = Depends(get_db), 
    current_admin = Depends(get_current_admin)
):
    service = EnquiryService(db)
    return service.get_all_enquiries()

@router.put("/{enquiry_id}", response_model=EnquiryAdminResponse)
def update_enquiry(
    enquiry_id: int, 
    enquiry_in: EnquiryUpdate, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    service = EnquiryService(db)
    updated_enquiry = service.update_enquiry(enquiry_id, enquiry_in)
    if not updated_enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return updated_enquiry

@router.websocket("/ws/live-enquiries")
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    from app.core.dependencies import get_current_user
    
    await manager.connect(websocket)
    try:
        # Check if the user is authenticated and is an Admin
        user = get_current_user(websocket, db) # Passing websocket as the request object
        if user.role_id != 1:
            await websocket.close(code=1008) # Policy Violation
            return

        while True:
            await websocket.receive_text() 
    except (HTTPException, JWTError):
        await websocket.close(code=1008)
    except WebSocketDisconnect:
        manager.disconnect(websocket)