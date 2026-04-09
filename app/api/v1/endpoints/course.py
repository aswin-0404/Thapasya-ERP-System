from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.services.course import CourseService
from app.utils.s3 import upload_file_to_s3

router = APIRouter()

# --- CREATE ---
@router.post("/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.create_course(course)

# --- READ ALL ---
@router.get("/", response_model=List[Course])
def get_courses(db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_all_courses()

# --- READ ONE ---
@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# --- UPDATE TEXT DETAILS ---
@router.patch("/{course_id}", response_model=Course)
def update_course_details(
    course_id: int, 
    course_data: CourseUpdate, 
    db: Session = Depends(get_db)
):
    """Update name, description, fee, etc."""
    service = CourseService(db)
    updated = service.update_course(course_id, course_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated

# --- UPDATE IMAGE ONLY ---
@router.patch("/{course_id}/image", response_model=Course)
async def update_course_image(
    course_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """Upload new image to S3 and update the course record."""
    # 1. Upload to S3
    url = upload_file_to_s3(file, folder="courses")
    if not url:
        raise HTTPException(status_code=500, detail="S3 Upload failed")

    # 2. Update DB
    service = CourseService(db)
    # We pass the dictionary; your Service handles the merge
    updated_course = service.update_course(course_id, {"image_url": url})
    
    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    return updated_course

# --- DEACTIVATE ---
@router.patch("/{course_id}/deactivate", response_model=Course)
def deactivate_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.deactivate_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# --- ACTIVATE ---
@router.patch("/{course_id}/activate", response_model=Course)
def activate_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.activate_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course