from fastapi import APIRouter
from app.api.v1.endpoints import student
from app.api.v1.endpoints import staff

api_router=APIRouter()


api_router.include_router(student.router,prefix="/student",tags=["Students"])
api_router.include_router(staff.router,prefix="/staff",tags=["Staff"])