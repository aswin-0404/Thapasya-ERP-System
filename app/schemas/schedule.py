from pydantic import BaseModel
from datetime import date,time

class ScheduleCreate(BaseModel):
    branch_id : int
    course_id : int
    staff_id : int
    class_date : date
    class_time : time