from fastapi import APIRouter
from app.api.v1.endpoints import student, staff, enquiry, course # Added yours here

api_router = APIRouter()

# Aswin's Routes
api_router.include_router(student.router, prefix="/student", tags=["Students"])
api_router.include_router(staff.router, prefix="/staff", tags=["Staff"])

# Your Routes (Integrated into the master router)
api_router.include_router(enquiry.router, prefix="/enquiries", tags=["Enquiries"])
api_router.include_router(course.router, prefix="/courses", tags=["Courses"])