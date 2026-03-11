from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas


def create_campus_info(db: Session, info_data: schemas.CampusInfoCreate):
    info = models.CampusInfo(**info_data.model_dump())
    db.add(info)
    db.commit()
    db.refresh(info)
    return info


def get_campus_info_by_id(db: Session, info_id: int):
    return db.query(models.CampusInfo).filter(models.CampusInfo.id == info_id).first()


def search_campus_info(db: Session, query: str):
    like_query = f"%{query}%"
    return (
        db.query(models.CampusInfo)
        .filter(
            or_(
                models.CampusInfo.title.ilike(like_query),
                models.CampusInfo.category.ilike(like_query),
                models.CampusInfo.content.ilike(like_query),
            )
        )
        .order_by(models.CampusInfo.title.asc())
        .all()
    )


def get_all_campus_info(db: Session):
    return db.query(models.CampusInfo).order_by(models.CampusInfo.title.asc()).all()


def update_campus_info(db: Session, info_id: int, info_data: schemas.CampusInfoUpdate):
    info = get_campus_info_by_id(db, info_id)
    if not info:
        return None
    for field, value in info_data.model_dump(exclude_unset=True).items():
        setattr(info, field, value)
    db.commit()
    db.refresh(info)
    return info


def delete_campus_info(db: Session, info_id: int):
    info = get_campus_info_by_id(db, info_id)
    if not info:
        return None
    db.delete(info)
    db.commit()
    return info
