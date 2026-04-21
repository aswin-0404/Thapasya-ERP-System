from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.student import StudentRegisterSchema
from app.services.student_service import register_student, get_student_enrolled_courses, get_student_home_dashboard
from app.db.session import get_db
from app.core.dependencies import get_current_admin, get_current_user

router = APIRouter()

# Register Student
@router.post("/register-student")
def register(data: StudentRegisterSchema, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    try:
        return register_student(db, data, current_admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Enrolled Courses
@router.get("/my-courses")
def get_my_courses(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return get_student_enrolled_courses(db, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Home Dashboard Data
@router.get("/dashboard/{course_id}")
def get_dashboard(course_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return get_student_home_dashboard(db, current_user, course_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))