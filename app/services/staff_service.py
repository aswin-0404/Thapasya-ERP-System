from app.models.staff import Staff
from app.models.staff_account import StaffAccount
from app.models.staff_course import StaffCourse
from app.repositories.user_repository import create_user
from app.core.security import hash_password

def register_staff(db,data):
    try:
        hashed_password=hash_password(data.password)

        user = create_user(
            db,
            data.username,
            data.email,
            hashed_password,
            data.role_id
        )
        db.flush()

        staff = Staff(
            user_id=user.id,
            name=data.staff.name,
            phone=data.staff.phone,
            branch_id=data.staff.branch_id,
            adhar_url=data.staff.aadhar_url
        )
        db.add(staff)
        db.flush()

        for course_id in data.course_ids:
            db.add(StaffCourse(
                staff_id = staff.id,
                course_id = course_id
            ))

        account= StaffAccount(
            staff_id=staff.id,
            account_number = data.account.account_number,
            ifsc = data.account.ifsc
        )
        db.add(account)

        db.commit()

        return {"message":"staff registerd successfully"}
    
    except Exception as e:
        db.rollback()
        raise e
    