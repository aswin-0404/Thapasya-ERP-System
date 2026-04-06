from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.staff import StaffRegisterSchema
from app.services.staff_service import register_staff
from app.db.session import get_db

router = APIRouter()

@router.post("/register-staff")
def register(data:StaffRegisterSchema, db:Session =Depends(get_db)):
    try:
        return register_staff(db,data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))