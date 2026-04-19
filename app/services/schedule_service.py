from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.schedule import Schedule
from app.models.staff import Staff
from app.models.course import Course
from app.models.branch import Branch
from app.models.staff_course import StaffCourse

def create_schedule_service(data, db :Session):

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
    


    
