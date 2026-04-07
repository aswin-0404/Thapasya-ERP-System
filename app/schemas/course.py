from pydantic import BaseModel, field_validator
from typing import Optional

class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    fee: Optional[float] = None
    is_active: bool = True
    image_url: Optional[str] = None
    min_age: int = 5

    @field_validator("min_age")
    def validate_min_age(cls, v):
        if v < 5:
            raise ValueError("Minimum age must be 5 or above")
        return v

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fee: Optional[float] = None
    image_url: Optional[str] = None
    min_age: Optional[int] = None

    @field_validator("min_age")
    def validate_min_age(cls, v):
        if v is not None and v < 5:
            raise ValueError("Minimum age must be 5 or above")
        return v


class Course(CourseCreate):
    id: int

    class Config:
        from_attributes = True