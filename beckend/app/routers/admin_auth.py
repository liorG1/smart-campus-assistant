import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.auth import create_access_token, hash_password, verify_password
from app.crud.admin import (
    create_admin,
    get_admin_by_email,
    get_admin_by_username,
)
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Auth"])

logger = logging.getLogger(__name__)


@router.post("/register", response_model=schemas.AdminRead, status_code=status.HTTP_201_CREATED)
def register_admin(
    admin_data: schemas.AdminCreate,
    db: Session = Depends(get_db),
):
    logger.info("Admin registration attempt | username=%s", admin_data.username)

    existing_username = get_admin_by_username(db, admin_data.username)
    if existing_username:
        logger.warning("Admin registration failed | username already exists | username=%s", admin_data.username)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    existing_email = get_admin_by_email(db, admin_data.email)
    if existing_email:
        logger.warning("Admin registration failed | email already exists | email=%s", admin_data.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    password_hash = hash_password(admin_data.password)
    admin = create_admin(db, admin_data, password_hash)
    logger.info("Admin registered successfully | admin_id=%s | username=%s", admin.id, admin.username)
    return admin


@router.post("/login", response_model=schemas.Token)
def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    logger.info("Admin login attempt | username=%s", form_data.username)

    admin = get_admin_by_username(db, form_data.username)

    if not admin or not verify_password(form_data.password, admin.password_hash):
        logger.warning("Admin login failed | invalid credentials | username=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not admin.is_active:
        logger.warning("Admin login failed | inactive admin | username=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive",
        )

    access_token = create_access_token(data={"sub": str(admin.id)})
    logger.info("Admin login successful | admin_id=%s | username=%s", admin.id, admin.username)

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me", response_model=schemas.AdminRead)
def get_me(current_admin=Depends(get_current_admin)):
    logger.info("Admin profile fetched | admin_id=%s | username=%s", current_admin.id, current_admin.username)
    return current_admin