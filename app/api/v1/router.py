from fastapi import APIRouter
from app.api.v1.endpoints import student, staff, enquiry, course, booking, auth

api_router = APIRouter()

# Aswin Routes

api_router.include_router(student.router, prefix="/student", tags=["Students"])
api_router.include_router(staff.router, prefix="/staff", tags=["Staff"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])


# Prince Routes

api_router.include_router(enquiry.router, prefix="/enquiries", tags=["Enquiries"])
api_router.include_router(course.router, prefix="/courses", tags=["Courses"])
api_router.include_router(booking.router, prefix="/bookings", tags=["Bookings"])