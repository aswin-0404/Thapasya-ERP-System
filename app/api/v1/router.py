from app.api.v1.endpoints import student
from fastapi import APIRouter


api_router=APIRouter()


api_router.include_router(student.router,prefix="/student",tags=["Students"])