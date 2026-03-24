from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from app.db.base import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String)
    password=Column(String)
    role_id=Column(Integer,ForeignKey("roles.id"))
    is_active=Column(Boolean,default=True)
    