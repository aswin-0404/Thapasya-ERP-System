from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.services.staff_service import  staff_course_toggle

router=APIRouter(prefix="/my-courses",tags=["Specific Staff Courses"])

@router.get("/")
def get_my_courses(db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return staff_course_toggle(db,current_user)
    