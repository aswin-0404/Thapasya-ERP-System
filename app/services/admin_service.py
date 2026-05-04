from fastapi import HTTPException
from app.models.student import Student
from sqlalchemy.orm import Session

from app.models.student_course import StudentCourse
from app.models.fee import FeeSchedule

def student_list(db : Session ,current_admin):
    try:
        student=db.query(Student).all()

        if not student:
            return {"message":"No students Found"}
        
        return [
            {
            "id":s.id,
            "name":s.name,
            "user_name":s.user.username,
            "branch":s.branch.name
        }
        for s in student
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
def get_student_details(student_id, db: Session , current_admin):
    try:
        student=db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return{"message":"Student not found"}
        
        stud_course= db.query(StudentCourse).filter(StudentCourse.student_id == student_id).all()

        fee_details=db.query(FeeSchedule).filter(FeeSchedule.student_id == student_id).limit(5).all()
        
        return{
            "name":student.name,
            "phone":student.phone,
            "dob":student.dob,
            "address":student.address,
            "courses":[
                {"name":c.course.name}
                for c in stud_course
            ],
            "fee_details":[{
                "course":f.course.name,
                "amount":f.amount,
                "due":f.due_date,
                "status":f.status

            }
            for f in fee_details
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))