from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.staff import Staff
from app.models.course import Course
from app.models.staff_course import StaffCourse
from app.core.dependencies import get_current_user

router=APIRouter(prefix="/my-courses",tags=["Specific Staff Courses"])

@router.get("/")
def get_my_courses(db:Session = Depends(get_db),current_user=Depends(get_current_user)):

    staff=db.query(Staff).filter(Staff.user_id == current_user.id).first()

    courses = db.query(Course).join(StaffCourse).filter(StaffCourse.staff_id == staff.id).all()

    return courses