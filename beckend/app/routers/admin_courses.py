from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.crud.courses import create_course, delete_course, get_all_courses, update_course
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/courses", tags=["Admin Courses"])


@router.get("/", response_model=list[schemas.CourseRead])
def list_courses(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_courses(db)


@router.post("/", response_model=schemas.CourseRead, status_code=status.HTTP_201_CREATED)
def create_course_route(
    course_data: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    try:
        return create_course(db, course_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course code already exists")


@router.put("/{course_id}", response_model=schemas.CourseRead)
def update_course_route(
    course_id: int,
    course_data: schemas.CourseUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    try:
        course = update_course(db, course_id, course_data)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course update violates uniqueness rules")


@router.delete("/{course_id}")
def delete_course_route(course_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    course = delete_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
