from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Staff(Base):
    __tablename__="staff"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    branch_id = Column(Integer,ForeignKey("branches.id"))

    name = Column(String)
    phone = Column(String)
    adhar_url= Column(String)

    user=relationship("User")
    branch=relationship("Branch")

