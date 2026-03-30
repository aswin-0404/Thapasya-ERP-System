from sqlalchemy import Column,Integer,String
from app.db.base_class import Base

class Parent(Base):
    __tablename__="parents"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    phone=Column(String)
    email=Column(String,nullable=True)
    