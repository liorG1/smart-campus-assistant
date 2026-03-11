from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import models, schemas


def create_office_hours(db: Session, office_hours_data: schemas.OfficeHoursCreate):
    office_hours = models.OfficeHours(**office_hours_data.model_dump())
    db.add(office_hours)
    db.commit()
    db.refresh(office_hours)
    return office_hours


def get_office_hours_by_id(db: Session, office_hours_id: int):
    return (
        db.query(models.OfficeHours)
        .options(joinedload(models.OfficeHours.building), joinedload(models.OfficeHours.room))
        .filter(models.OfficeHours.id == office_hours_id)
        .first()
    )


def get_office_hours_by_staff_name(db: Session, staff_name: str):
    like_query = f"%{staff_name}%"
    return (
        db.query(models.OfficeHours)
        .options(joinedload(models.OfficeHours.building), joinedload(models.OfficeHours.room))
        .filter(models.OfficeHours.staff_name.ilike(like_query))
        .order_by(models.OfficeHours.day_of_week.asc(), models.OfficeHours.start_time.asc())
        .all()
    )


def get_office_hours_by_office_name(db: Session, office_name: str):
    like_query = f"%{office_name}%"
    return (
        db.query(models.OfficeHours)
        .options(joinedload(models.OfficeHours.building), joinedload(models.OfficeHours.room))
        .filter(models.OfficeHours.office_name.ilike(like_query))
        .order_by(models.OfficeHours.day_of_week.asc(), models.OfficeHours.start_time.asc())
        .all()
    )


def search_office_hours(db: Session, query: str):
    like_query = f"%{query}%"
    return (
        db.query(models.OfficeHours)
        .options(joinedload(models.OfficeHours.building), joinedload(models.OfficeHours.room))
        .outerjoin(models.Building, models.OfficeHours.building_id == models.Building.id)
        .outerjoin(models.Room, models.OfficeHours.room_id == models.Room.id)
        .filter(
            or_(
                models.OfficeHours.staff_name.ilike(like_query),
                models.OfficeHours.office_name.ilike(like_query),
                models.OfficeHours.day_of_week.ilike(like_query),
                models.OfficeHours.notes.ilike(like_query),
                models.Building.name.ilike(like_query),
                models.Room.room_number.ilike(like_query),
            )
        )
        .order_by(models.OfficeHours.staff_name.asc())
        .all()
    )


def get_all_office_hours(db: Session):
    return (
        db.query(models.OfficeHours)
        .options(joinedload(models.OfficeHours.building), joinedload(models.OfficeHours.room))
        .order_by(models.OfficeHours.staff_name.asc(), models.OfficeHours.day_of_week.asc())
        .all()
    )


def update_office_hours(db: Session, office_hours_id: int, office_hours_data: schemas.OfficeHoursUpdate):
    office_hours = get_office_hours_by_id(db, office_hours_id)
    if not office_hours:
        return None
    for field, value in office_hours_data.model_dump(exclude_unset=True).items():
        setattr(office_hours, field, value)
    db.commit()
    db.refresh(office_hours)
    return office_hours


def delete_office_hours(db: Session, office_hours_id: int):
    office_hours = get_office_hours_by_id(db, office_hours_id)
    if not office_hours:
        return None
    db.delete(office_hours)
    db.commit()
    return office_hours
