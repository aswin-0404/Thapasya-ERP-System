from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.services.course import CourseService

router = APIRouter()

# Create a new course
@router.post("/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.create_course(course)

# Get all Courses
@router.get("/", response_model=List[Course])
def get_courses(db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_all_courses()

# Get individual Courses
@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Update Courses
@router.patch("/{course_id}", response_model=Course)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    service = CourseService(db)
    updated = service.update_course(course_id, course)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated

# Deactivate a course (soft delete)
@router.patch("/{course_id}/deactivate", response_model=Course)
def deactivate_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.deactivate_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Restores a deactivated course
@router.patch("/{course_id}/activate", response_model=Course)
def activate_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.activate_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course