from sqlalchemy import Column,Integer,String,ForeignKey
from app.db.base import Base

class StaffAccount(Base):
    __tablename__="staff_accounts"

    id= Column(Integer,primary_key=True,index=True)
    staff_id= Column(Integer,ForeignKey("staff.id"))

    account_number= Column(String)
    ifsc = Column(String)