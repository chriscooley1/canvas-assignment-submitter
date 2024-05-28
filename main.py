# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from models import Course, Assignment

app = FastAPI()

courses = {}
assignments = {}

@app.post("/courses", response_model=Course)
async def create_course(course: Course) -> Course:
    courses[course.course_id] = course
    return course

@app.get("/courses", response_model=List[Course])
async def get_courses() -> List[Course]:
    return list(courses.values())

@app.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: int) -> Course:
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.post("/courses/{course_id}/assignments", response_model=Assignment)
async def create_assignment(course_id: int, assignment: Assignment) -> Assignment:
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    assignments.setdefault(course_id, {})
    assignments[course_id][assignment.assignment_id] = assignment
    return assignment

@app.get("/courses/{course_id}/assignments", response_model=List[Assignment])
async def get_assignments(course_id: int) -> List[Assignment]:
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return list(assignments.get(course_id, {}).values())

@app.post("/courses/{course_id}/assignments/{assignment_id}/submit")
async def submit_assignment(course_id: int, assignment_id: int, submission_data: dict) -> dict:
    if course_id not in courses or assignment_id not in assignments.get(course_id, {}):
        raise HTTPException(status_code=404, detail="Course or Assignment not found")
    return submission_data
