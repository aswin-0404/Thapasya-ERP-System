from sqlalchemy import Column,String,Integer
from app.db.base_class import Base

class Course(Base):
    __tablename__="courses"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)