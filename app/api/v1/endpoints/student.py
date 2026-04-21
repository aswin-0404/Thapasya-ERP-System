from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.student import StudentRegisterSchema
from app.services.student_service import register_student
from app.db.session import get_db
from app.core.dependencies import get_current_admin


router=APIRouter()

@router.post("/register-student")
def register(data:StudentRegisterSchema, db:Session = Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return register_student(db,data,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
