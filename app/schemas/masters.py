from pydantic import BaseModel

class RoleCreate(BaseModel):
    name : str

class BranchCreate(BaseModel):
    name : str
    location : str