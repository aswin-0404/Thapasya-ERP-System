from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.services.staff_service import  staff_course_toggle,get_my_students_service

from app.schemas.attendance import AttendanceCreate
from app.services.staff_service import mark_attendance_service


router=APIRouter(prefix="/staff",tags=["Specific Staff Datas"])

@router.get("/my-courses")
def get_my_courses(db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return staff_course_toggle(db,current_user)
    

@router.get("/my-students")
def get_my_students(course_id : int,branch_id : int,db : Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return get_my_students_service(course_id,branch_id,db,current_user)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.post('/mark-attendance')
def mark_student_attendance(data : AttendanceCreate, db : Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return mark_attendance_service(data,db,current_user)
    except Exception as e:
        raise HTTPException (status_code=400,detail=str(e))