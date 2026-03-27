from sqlalchemy.orm import declarative_base

Base=declarative_base()


from app.models.branch import Branch
from app.models.course import Course
from app.models.parent import Parent
from app.models.role import Role
from app.models.staff_account import StaffAccount
from app.models.staff_course import StaffCourse
from app.models.staff import Staff
from app.models.student_course import StudentCourse
from app.models.student import Student
from app.models.user import User