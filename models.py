from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    course_id: int
    name: str
    year: int

class Assignment(BaseModel):
    assignment_id: int
    name: str
    description: Optional[str] = None
