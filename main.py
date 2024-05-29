from fastapi import FastAPI, HTTPException, Path, Body
from typing import List, Dict
from models import Course, Assignment

app = FastAPI()

# In-memory storage for courses and assignments
courses: Dict[int, Course] = {}
assignments: Dict[int, Dict[int, Assignment]] = {}

@app.post("/courses", response_model=Course)
async def create_course(course: Course):
    if course.course_id in courses:
        raise HTTPException(status_code=400, detail="Course already exists")
    courses[course.course_id] = course
    return course

@app.get("/courses", response_model=List[Course])
async def get_courses():
    return list(courses.values())

@app.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.post("/courses/{course_id}/assignments", response_model=Assignment)
async def create_assignment(course_id: int, assignment: Assignment):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    if course_id not in assignments:
        assignments[course_id] = {}
    if assignment.assignment_id in assignments[course_id]:
        raise HTTPException(status_code=400, detail="Assignment already exists")
    assignments[course_id][assignment.assignment_id] = assignment
    return assignment

@app.get("/courses/{course_id}/assignments", response_model=List[Assignment])
async def get_assignments(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return list(assignments.get(course_id, {}).values())

@app.put("/courses/{course_id}/assignments/{assignment_id}/submit")
async def update_assignment(course_id: int, assignment_id: int, assignment: Assignment):
    if course_id not in courses or assignment_id not in assignments.get(course_id, {}):
        raise HTTPException(status_code=404, detail="Course or Assignment not found")
    assignments[course_id][assignment_id] = assignment
    return {"message": "Assignment updated successfully"}

@app.delete("/courses/{course_id}/assignments/{assignment_id}/submit")
async def delete_assignment(course_id: int, assignment_id: int):
    if course_id not in courses or assignment_id not in assignments.get(course_id, {}):
        raise HTTPException(status_code=404, detail="Course or Assignment not found")
    del assignments[course_id][assignment_id]
    return {"message": "Assignment deleted successfully"}
