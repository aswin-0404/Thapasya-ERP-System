from fastapi import APIRouter
from app.api.v1.endpoints import enquiry, course, booking

from app.api.v1.endpoints.student import router as student_router
from app.api.v1.endpoints.staff import router as staff_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.role import router as role_router
from app.api.v1.endpoints.branch import router as branch_router

api_router = APIRouter()

# Aswin Routes

api_router.include_router(student_router, prefix="/student", tags=["Students"])
api_router.include_router(staff_router, prefix="/staff", tags=["Staff"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(role_router)   
api_router.include_router(branch_router)


# Prince Routes

api_router.include_router(enquiry.router, prefix="/enquiries", tags=["Enquiries"])
api_router.include_router(course.router, prefix="/courses", tags=["Courses"])
api_router.include_router(booking.router, prefix="/bookings", tags=["Bookings"])