from app.models.parent import Parent
from app.models.student import Student
from app.models.student_course import StudentCourse
from app.repositories.user_repository import create_user
from app.core.security import hash_password

def register_student(db,data,current_admin):
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

        parent = db.query(Parent).filter(
            Parent.phone== data.parent.phone,
            Parent.name == data.parent.name
        ).first()

        if not parent:
            parent= Parent(
                name=data.parent.name,
                phone=data.parent.phone,
                email=data.parent.email
            )
            db.add(parent)
            db.flush()

        student= Student(
            user_id=user.id,
            parent_id=parent.id,
            branch_id=data.student.branch_id,
            name=data.student.name,
            phone=data.student.phone,
        )
        db.add(student)
        db.flush()


        for course_id in data.course_ids:
            db.add(StudentCourse(
                student_id = student.id,
                course_id=course_id
            ))
        
        db.commit()

        return {"message":"Student registration successfull"}
    
    except Exception as e:
        db.rollback()
        raise e