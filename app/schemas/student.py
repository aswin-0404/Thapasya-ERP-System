from pydantic import BaseModel,EmailStr
from typing import List


class ParentSchema(BaseModel):
    name:str
    phone:str
    email:EmailStr | None=None

class StudentDataSchema(BaseModel):
    name: str
    phone: str
    dob: str
    branch_id: int

class StudentRegisterSchema(BaseModel):
    username : str
    password: str
    email : EmailStr | None = None
    role_id : int

    parent:ParentSchema
    student:StudentDataSchema
    course_ids: List[int]

