from sqlalchemy import Column,Integer,String,ForeignKey
from app.db.base import Base

class StudentCourse(Base):
    __tablename__="student_courses"

    id= Column(Integer,primary_key=True,index=True)
    student_id= Column(Integer,ForeignKey("students.id"))
    course_id= Column(Integer,ForeignKey("courses.id"))