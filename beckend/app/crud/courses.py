from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas


def create_course(db: Session, course_data: schemas.CourseCreate):
    course = models.Course(**course_data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_code(db: Session, course_code: str):
    return db.query(models.Course).filter(models.Course.course_code.ilike(course_code)).first()


def get_course_by_name(db: Session, course_name: str):
    return db.query(models.Course).filter(models.Course.course_name.ilike(course_name)).first()


def search_courses(db: Session, query: str):
    like_query = f"%{query}%"
    return (
        db.query(models.Course)
        .filter(
            or_(
                models.Course.course_code.ilike(like_query),
                models.Course.course_name.ilike(like_query),
            )
        )
        .order_by(models.Course.course_name.asc())
        .all()
    )


def get_all_courses(db: Session):
    return db.query(models.Course).order_by(models.Course.course_name.asc()).all()


def update_course(db: Session, course_id: int, course_data: schemas.CourseUpdate):
    course = get_course_by_id(db, course_id)
    if not course:
        return None
    for field, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int):
    course = get_course_by_id(db, course_id)
    if not course:
        return None
    db.delete(course)
    db.commit()
    return course
