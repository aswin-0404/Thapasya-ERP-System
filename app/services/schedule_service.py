from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.schedule import Schedule
from app.models.staff import Staff
from app.models.course import Course
from app.models.branch import Branch
from app.models.staff_course import StaffCourse
from datetime import date
from app.core.dependencies import check_admin_role,check_user_role

def create_schedule_service(data, db :Session,current_admin):

    role=check_admin_role(db,current_admin)
    if role != "admin":
        raise HTTPException(status_code=403,detail="Admin only can access")


    branch=db.query(Branch).filter(Branch.id == data.branch_id).first()
    if not branch:
        raise HTTPException(status_code=404 ,detail="Branch not found")

    course=db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404 ,detail="Course not found")

    staff=db.query(Staff).filter(Staff.id == data.staff_id).first()
    if not staff:
        raise HTTPException(status_code=404 ,detail="Staff not found")
    
    if staff.branch_id != data.branch_id:
        raise HTTPException(status_code=400 ,detail="Staff not belongs to this Branch")

    existing= db.query(Schedule).filter(
        Schedule.staff_id == data.staff_id,
        Schedule.class_date == data.class_date,
        Schedule.class_time == data.class_time
    ).first()

    assigned = db.query(StaffCourse).filter(
    StaffCourse.staff_id == data.staff_id,
    StaffCourse.course_id == data.course_id).first()

    if not assigned:
        raise HTTPException(400, "Staff is not assigned to this course")

    if existing:
        raise HTTPException(status_code=400,detail="Schedule already exists at this time for this staff")
    
    schedule=Schedule(
        branch_id=data.branch_id,
        course_id=data.course_id,
        staff_id=data.staff_id,
        class_date=data.class_date,
        class_time=data.class_time
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule
    

def get_upcoming_schedule_service(course_id : int ,db : Session, current_user):

    role=check_user_role(db,current_user)
    if role != "staff":
        raise HTTPException(status_code=403,detail="staff only can access")
    
    staff=db.query(Staff).filter(Staff.user_id == current_user.id).first()
    if not staff:
        raise HTTPException(status_code=404,detail="Staff not found")
    
    today = date.today()

    schedule=db.query(Schedule).filter(
        Schedule.staff_id == staff.id,
        Schedule.course_id == course_id,
        Schedule.class_date >= today
    ).order_by(Schedule.class_date,Schedule.class_time).all()

    if not schedule:
        return{
            "message":"No schedules Available"
        }
    
    return [
        {
            "class_date":s.class_date,
            "class_time": s.class_time,
            "course":s.course.name
        }
        for s in schedule
    ]
    
