from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud.courses import get_course_by_id
from app.crud.exam_schedules import create_exam_schedule, delete_exam_schedule, get_all_exam_schedules, update_exam_schedule
from app.crud.rooms import get_room_by_id
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/exams", tags=["Admin Exam Schedules"])


@router.get("/", response_model=list[schemas.ExamScheduleRead])
def list_exam_schedules(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_exam_schedules(db)


@router.post("/", response_model=schemas.ExamScheduleRead, status_code=status.HTTP_201_CREATED)
def create_exam_schedule_route(
    exam_data: schemas.ExamScheduleCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    if not get_course_by_id(db, exam_data.course_id):
        raise HTTPException(status_code=400, detail="Course does not exist")
    if exam_data.room_id is not None and not get_room_by_id(db, exam_data.room_id):
        raise HTTPException(status_code=400, detail="Room does not exist")
    return create_exam_schedule(db, exam_data)


@router.put("/{exam_id}", response_model=schemas.ExamScheduleRead)
def update_exam_schedule_route(
    exam_id: int,
    exam_data: schemas.ExamScheduleUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    if exam_data.course_id is not None and not get_course_by_id(db, exam_data.course_id):
        raise HTTPException(status_code=400, detail="Course does not exist")
    if exam_data.room_id is not None and not get_room_by_id(db, exam_data.room_id):
        raise HTTPException(status_code=400, detail="Room does not exist")

    exam = update_exam_schedule(db, exam_id, exam_data)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    return exam


@router.delete("/{exam_id}")
def delete_exam_schedule_route(exam_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    exam = delete_exam_schedule(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    return {"message": "Exam schedule deleted successfully"}
