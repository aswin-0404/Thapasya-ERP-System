from app.db.base_class import Base
from sqlalchemy import Column,Integer,ForeignKey,Date,Enum,String
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import UniqueConstraint

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class Attendance(Base):
    __tablename__="attendance"

    __table_args__ = (
    UniqueConstraint("student_id", "course_id", "date", name="unique_attendance"),
    )

    id = Column(Integer,primary_key=True,index=True)

    student_id = Column(Integer,ForeignKey("students.id"),nullable=False)
    course_id = Column(Integer,ForeignKey("courses.id"),nullable=False)

    date = Column(Date,nullable=False)
    status = Column(Enum(AttendanceStatus),nullable=False)

    student= relationship("Student")
    course= relationship("Course")