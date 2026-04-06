from pydantic import BaseModel,EmailStr
from typing import List

class StaffDataSchema(BaseModel):
    name : str
    phone : str
    branch_id : int
    aadhar_url : str | None=None

class StaffAccountSchema(BaseModel):
    account_number : str
    ifsc : str

class StaffRegisterSchema(BaseModel):
    username : str
    password : str
    email : EmailStr 
    role_id : int

    staff : StaffDataSchema
    course_ids : List[int]
    account : StaffAccountSchema