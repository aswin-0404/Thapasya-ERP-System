from fastapi import HTTPException

from app.models.student import Student
from app.models.staff import Staff
from app.models.staff_account import StaffAccount
from app.core.dependencies import check_user_role
from sqlalchemy.orm import joinedload

def get_profile(db,current_user):
    try:
        role=check_user_role(db,current_user)
        if role == "staff":

            result = db.query(Staff, StaffAccount).outerjoin(
                StaffAccount, StaffAccount.staff_id == Staff.id
                ).filter(
                    Staff.user_id == current_user.id
                ).first()

            if not result:
                raise HTTPException(status_code=404, detail="Staff not found")
            
            staff,account=result


            return {
                "name":staff.name,
                "phone":staff.phone,
                "address":staff.address if staff.address else None,
                "email":staff.user.email if staff.user else None,
                "account_details":{
                    "acc_no":account.account_number if account else None,
                    "ifsc":account.ifsc if account else None
                }
            }
        
        elif role == "student":
            student=db.query(Student).filter(
                Student.user_id == current_user.id
            ).first()

            parent=student.parent


            if not student:
                raise HTTPException(status_code=404, detail="Student not found")

            return{
                "name":student.name,
                "phone":student.phone,
                "address":student.address,
                "email":student.user.email if student.user else None,
                "parent":{
                    "name":parent.name,
                    "phone":parent.phone,
                    "email":parent.email
                }
            }
        else:
            return {
                "message":"User not found"
            }
        
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
