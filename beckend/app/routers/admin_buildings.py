from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.crud.buildings import create_building, delete_building, get_all_buildings, update_building
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/buildings", tags=["Admin Buildings"])


@router.get("/", response_model=list[schemas.BuildingRead])
def list_buildings(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_buildings(db)


@router.post("/", response_model=schemas.BuildingRead, status_code=status.HTTP_201_CREATED)
def create_building_route(
    building_data: schemas.BuildingCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    try:
        return create_building(db, building_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Building name or code already exists")


@router.put("/{building_id}", response_model=schemas.BuildingRead)
def update_building_route(
    building_id: int,
    building_data: schemas.BuildingUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    try:
        building = update_building(db, building_id, building_data)
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        return building
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Building update violates uniqueness rules")


@router.delete("/{building_id}")
def delete_building_route(
    building_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    building = delete_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"message": "Building deleted successfully"}
