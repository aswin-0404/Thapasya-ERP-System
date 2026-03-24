from sqlalchemy import Column,Integer,String
from app.db.base import Base

class Branch(Base):
    __tablename__="branches"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    location=Column(String)