from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import models, schemas


def create_room(db: Session, room_data: schemas.RoomCreate):
    room = models.Room(**room_data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def get_room_by_id(db: Session, room_id: int):
    return (
        db.query(models.Room)
        .options(joinedload(models.Room.building))
        .filter(models.Room.id == room_id)
        .first()
    )


def get_room_by_number_and_building(db: Session, room_number: str, building_id: int):
    return (
        db.query(models.Room)
        .filter(models.Room.room_number.ilike(room_number), models.Room.building_id == building_id)
        .first()
    )


def search_rooms(db: Session, query: str):
    like_query = f"%{query}%"
    return (
        db.query(models.Room)
        .options(joinedload(models.Room.building))
        .join(models.Building)
        .filter(
            or_(
                models.Room.room_number.ilike(like_query),
                models.Building.name.ilike(like_query),
                models.Building.code.ilike(like_query),
                models.Room.description.ilike(like_query),
            )
        )
        .order_by(models.Building.name.asc(), models.Room.room_number.asc())
        .all()
    )


def get_rooms_by_building_id(db: Session, building_id: int):
    return (
        db.query(models.Room)
        .filter(models.Room.building_id == building_id)
        .order_by(models.Room.room_number.asc())
        .all()
    )


def get_all_rooms(db: Session):
    return (
        db.query(models.Room)
        .options(joinedload(models.Room.building))
        .order_by(models.Room.id.asc())
        .all()
    )


def update_room(db: Session, room_id: int, room_data: schemas.RoomUpdate):
    room = get_room_by_id(db, room_id)
    if not room:
        return None
    for field, value in room_data.model_dump(exclude_unset=True).items():
        setattr(room, field, value)
    db.commit()
    db.refresh(room)
    return room


def delete_room(db: Session, room_id: int):
    room = get_room_by_id(db, room_id)
    if not room:
        return None
    db.delete(room)
    db.commit()
    return room
