from sqlalchemy import Column,Integer,ForeignKey,Date,Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import date

class DailyLog(Base):
    __tablename__="daily_logs"

    id=Column(Integer,primary_key=True,index=True)
    date=Column(Date,default=date.today,nullable=False)

    staff_id=Column(Integer,ForeignKey("staff.id"),nullable=False)
    course_id=Column(Integer,ForeignKey("courses.id"),nullable=False)

    class_summary = Column(Text)
    topics_covered = Column(Text)
    next_class_topic = Column(Text)

    staff=relationship("Staff")
    course = relationship("Course")