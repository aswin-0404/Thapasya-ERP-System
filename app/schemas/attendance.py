from pydantic import BaseModel
from app.models.attendence import AttendanceStatus

class AttendanceCreate(BaseModel):
    student_id : int
    course_id : int
    status : AttendanceStatus