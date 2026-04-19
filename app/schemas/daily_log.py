from pydantic import BaseModel
from datetime import date

class DailyLogCreate(BaseModel):
    course_id : int
    class_summary : str
    topics_covered : str
    next_class_topic : str
