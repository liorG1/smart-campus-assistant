from sqlalchemy.orm import Session, joinedload

from app import models, schemas


def create_exam_schedule(db: Session, exam_data: schemas.ExamScheduleCreate):
    exam = models.ExamSchedule(**exam_data.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def get_exam_schedule_by_id(db: Session, exam_id: int):
    return (
        db.query(models.ExamSchedule)
        .options(
            joinedload(models.ExamSchedule.course),
            joinedload(models.ExamSchedule.room).joinedload(models.Room.building),
        )
        .filter(models.ExamSchedule.id == exam_id)
        .first()
    )


def get_exam_schedules_by_course_id(db: Session, course_id: int):
    return (
        db.query(models.ExamSchedule)
        .options(
            joinedload(models.ExamSchedule.course),
            joinedload(models.ExamSchedule.room).joinedload(models.Room.building),
        )
        .filter(models.ExamSchedule.course_id == course_id)
        .order_by(models.ExamSchedule.exam_date.asc(), models.ExamSchedule.exam_time.asc())
        .all()
    )


def get_exam_schedules_by_course_name(db: Session, course_name: str):
    like_query = f"%{course_name}%"
    return (
        db.query(models.ExamSchedule)
        .options(
            joinedload(models.ExamSchedule.course),
            joinedload(models.ExamSchedule.room).joinedload(models.Room.building),
        )
        .join(models.Course)
        .filter(models.Course.course_name.ilike(like_query))
        .order_by(models.ExamSchedule.exam_date.asc(), models.ExamSchedule.exam_time.asc())
        .all()
    )


def get_exam_schedules_by_course_code(db: Session, course_code: str):
    like_query = f"%{course_code}%"
    return (
        db.query(models.ExamSchedule)
        .options(
            joinedload(models.ExamSchedule.course),
            joinedload(models.ExamSchedule.room).joinedload(models.Room.building),
        )
        .join(models.Course)
        .filter(models.Course.course_code.ilike(like_query))
        .order_by(models.ExamSchedule.exam_date.asc(), models.ExamSchedule.exam_time.asc())
        .all()
    )


def get_all_exam_schedules(db: Session):
    return (
        db.query(models.ExamSchedule)
        .options(
            joinedload(models.ExamSchedule.course),
            joinedload(models.ExamSchedule.room).joinedload(models.Room.building),
        )
        .order_by(models.ExamSchedule.exam_date.asc(), models.ExamSchedule.exam_time.asc())
        .all()
    )


def update_exam_schedule(db: Session, exam_id: int, exam_data: schemas.ExamScheduleUpdate):
    exam = get_exam_schedule_by_id(db, exam_id)
    if not exam:
        return None
    for field, value in exam_data.model_dump(exclude_unset=True).items():
        setattr(exam, field, value)
    db.commit()
    db.refresh(exam)
    return exam


def delete_exam_schedule(db: Session, exam_id: int):
    exam = get_exam_schedule_by_id(db, exam_id)
    if not exam:
        return None
    db.delete(exam)
    db.commit()
    return exam
