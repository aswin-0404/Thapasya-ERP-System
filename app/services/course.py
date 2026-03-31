from sqlalchemy.orm import Session
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate

class CourseService:
    def __init__(self, db: Session):
        self.repository = CourseRepository(db)

    def create_course(self, course_data: CourseCreate):
        return self.repository.create(course_data)

    def get_all_courses(self):
        return self.repository.get_all()

    def get_course(self, course_id: int):
        return self.repository.get_by_id(course_id)
    
    def update_course(self, course_id: int, course_data):
        return self.repository.update(course_id, course_data)

    def deactivate_course(self, course_id: int):
        return self.repository.deactivate(course_id)

    def activate_course(self, course_id: int):
        return self.repository.activate(course_id)