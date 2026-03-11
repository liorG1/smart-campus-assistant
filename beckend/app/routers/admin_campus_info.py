from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud.campus_info import create_campus_info, delete_campus_info, get_all_campus_info, update_campus_info
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/campus-info", tags=["Admin Campus Info"])


@router.get("/", response_model=list[schemas.CampusInfoRead])
def list_campus_info(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_campus_info(db)


@router.post("/", response_model=schemas.CampusInfoRead, status_code=status.HTTP_201_CREATED)
def create_campus_info_route(
    info_data: schemas.CampusInfoCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return create_campus_info(db, info_data)


@router.put("/{info_id}", response_model=schemas.CampusInfoRead)
def update_campus_info_route(
    info_id: int,
    info_data: schemas.CampusInfoUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    info = update_campus_info(db, info_id, info_data)
    if not info:
        raise HTTPException(status_code=404, detail="Campus info record not found")
    return info


@router.delete("/{info_id}")
def delete_campus_info_route(info_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    info = delete_campus_info(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Campus info record not found")
    return {"message": "Campus info deleted successfully"}
