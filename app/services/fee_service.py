from fastapi import HTTPException
from datetime import date
from dateutil.relativedelta import relativedelta
from app.models.fee import FeeSchedule

from app.models.student_course import StudentCourse

def calculate_next_due(student_course,db):
    try:
        last_schedule=db.query(FeeSchedule).filter(
            FeeSchedule.student_id ==student_course.student_id,
            FeeSchedule.course_id == student_course.course_id
            ).order_by(FeeSchedule.due_date.desc()).first()

        if last_schedule:
            return last_schedule.due_date + relativedelta(months=1)
        else:
            return student_course.joined_date + relativedelta(months=1)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


def generate_next_month_fee(db,current_admin):
    try:
        student_courses=db.query(StudentCourse).all()

        for sc in student_courses:
            next_due=calculate_next_due(sc,db)

        exist=db.query(FeeSchedule).filter(
            FeeSchedule.student_id == sc.student_id,
            FeeSchedule.course_id == sc.course_id,
            FeeSchedule.due_date == next_due
        ).first()

        if not exist:
            db.add(FeeSchedule(
                student_id = sc.student_id,
                course_id = sc.course_id,
                due_date = next_due,
                amount = sc.course.fee
            ))

        db.commit()

        return {
            "message":"Fees scheduled successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    


    
