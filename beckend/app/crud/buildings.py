from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas


def create_building(db: Session, building_data: schemas.BuildingCreate):
    building = models.Building(**building_data.model_dump())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


def get_building_by_id(db: Session, building_id: int):
    return db.query(models.Building).filter(models.Building.id == building_id).first()


def get_building_by_name(db: Session, name: str):
    return db.query(models.Building).filter(models.Building.name.ilike(name)).first()


def get_building_by_code(db: Session, code: str):
    return db.query(models.Building).filter(models.Building.code.ilike(code)).first()


def search_buildings(db: Session, query: str):
    like_query = f"%{query}%"
    return (
        db.query(models.Building)
        .filter(
            or_(
                models.Building.name.ilike(like_query),
                models.Building.code.ilike(like_query),
                models.Building.address.ilike(like_query),
                models.Building.description.ilike(like_query),
            )
        )
        .order_by(models.Building.name.asc())
        .all()
    )


def get_all_buildings(db: Session):
    return db.query(models.Building).order_by(models.Building.name.asc()).all()


def update_building(db: Session, building_id: int, building_data: schemas.BuildingUpdate):
    building = get_building_by_id(db, building_id)
    if not building:
        return None
    for field, value in building_data.model_dump(exclude_unset=True).items():
        setattr(building, field, value)
    db.commit()
    db.refresh(building)
    return building


def delete_building(db: Session, building_id: int):
    building = get_building_by_id(db, building_id)
    if not building:
        return None
    db.delete(building)
    db.commit()
    return building
