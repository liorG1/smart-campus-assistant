from sqlalchemy.orm import Session

from app import models, schemas


def get_admin_by_id(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()


def get_admin_by_username(db: Session, username: str):
    return db.query(models.Admin).filter(models.Admin.username == username).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()


def get_all_admins(db: Session):
    return db.query(models.Admin).order_by(models.Admin.id.asc()).all()


def create_admin(db: Session, admin_data: schemas.AdminCreate, password_hash: str):
    admin = models.Admin(
        username=admin_data.username,
        email=admin_data.email,
        password_hash=password_hash,
        is_active=admin_data.is_active,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def update_admin_status(db: Session, admin_id: int, is_active: bool):
    admin = get_admin_by_id(db, admin_id)
    if not admin:
        return None
    admin.is_active = is_active
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin_id: int):
    admin = get_admin_by_id(db, admin_id)
    if not admin:
        return None
    db.delete(admin)
    db.commit()
    return admin
