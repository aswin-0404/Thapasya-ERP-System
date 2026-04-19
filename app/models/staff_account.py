from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class StaffAccount(Base):
    __tablename__="staff_accounts"

    id= Column(Integer,primary_key=True,index=True)
    staff_id= Column(Integer,ForeignKey("staff.id"))

    account_number= Column(String)
    ifsc = Column(String)

    staff=relationship("Staff")