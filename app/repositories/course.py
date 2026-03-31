from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, course_data: CourseCreate):
        db_course = Course(
            name=course_data.name,
            description=course_data.description,
            fee=course_data.fee,
            is_active=course_data.is_active,
            image_url=course_data.image_url,
            min_age=course_data.min_age
        )
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def get_all(self):
        return self.db.query(Course).filter(Course.is_active == True).all()

    def get_by_id(self, course_id: int):
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def update(self, course_id: int, course_data):
        db_course = self.get_by_id(course_id)
        if not db_course:
            return None
        update_fields = course_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(db_course, field, value)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def deactivate(self, course_id: int):
        db_course = self.get_by_id(course_id)
        if not db_course:
            return None
        db_course.is_active = False
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def activate(self, course_id: int):
        db_course = self.get_by_id(course_id)
        if not db_course:
            return None
        db_course.is_active = True
        self.db.commit()
        self.db.refresh(db_course)
        return db_course