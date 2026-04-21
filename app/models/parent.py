from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Parent(Base):
    __tablename__="parents"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    phone=Column(String,unique=True)
    email=Column(String,nullable=True)

    user_id=Column(Integer,ForeignKey("users.id"),nullable=True)

    students=relationship("Student",back_populates="parent")
    user=relationship("User")

