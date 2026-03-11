from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud.buildings import get_building_by_id
from app.crud.office_hours import create_office_hours, delete_office_hours, get_all_office_hours, update_office_hours
from app.crud.rooms import get_room_by_id
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/office-hours", tags=["Admin Office Hours"])


@router.get("/", response_model=list[schemas.OfficeHoursRead])
def list_office_hours(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_office_hours(db)


@router.post("/", response_model=schemas.OfficeHoursRead, status_code=status.HTTP_201_CREATED)
def create_office_hours_route(
    office_hours_data: schemas.OfficeHoursCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    if office_hours_data.building_id is not None and not get_building_by_id(db, office_hours_data.building_id):
        raise HTTPException(status_code=400, detail="Building does not exist")
    if office_hours_data.room_id is not None and not get_room_by_id(db, office_hours_data.room_id):
        raise HTTPException(status_code=400, detail="Room does not exist")
    return create_office_hours(db, office_hours_data)


@router.put("/{office_hours_id}", response_model=schemas.OfficeHoursRead)
def update_office_hours_route(
    office_hours_id: int,
    office_hours_data: schemas.OfficeHoursUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    if office_hours_data.building_id is not None and not get_building_by_id(db, office_hours_data.building_id):
        raise HTTPException(status_code=400, detail="Building does not exist")
    if office_hours_data.room_id is not None and not get_room_by_id(db, office_hours_data.room_id):
        raise HTTPException(status_code=400, detail="Room does not exist")

    record = update_office_hours(db, office_hours_id, office_hours_data)
    if not record:
        raise HTTPException(status_code=404, detail="Office hours record not found")
    return record


@router.delete("/{office_hours_id}")
def delete_office_hours_route(
    office_hours_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    record = delete_office_hours(db, office_hours_id)
    if not record:
        raise HTTPException(status_code=404, detail="Office hours record not found")
    return {"message": "Office hours deleted successfully"}
