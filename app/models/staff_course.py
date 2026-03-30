from sqlalchemy import Column,Integer,String,ForeignKey
from app.db.base_class import Base

class StaffCourse(Base):
    __tablename__="staff_courses"

    id= Column(Integer,primary_key=True,index=True)
    staff_id=Column(Integer,ForeignKey("staff.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))