from pydantic import BaseModel


class Course(BaseModel):
    course_id: int
    name: str
    year: int

class Assignment(BaseModel):
    assignment_id: int
    name: str