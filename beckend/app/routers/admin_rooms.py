from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.crud.buildings import get_building_by_id
from app.crud.rooms import create_room, delete_room, get_all_rooms, update_room
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/rooms", tags=["Admin Rooms"])


@router.get("/", response_model=list[schemas.RoomRead])
def list_rooms(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_rooms(db)


@router.post("/", response_model=schemas.RoomRead, status_code=status.HTTP_201_CREATED)
def create_room_route(
    room_data: schemas.RoomCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    if not get_building_by_id(db, room_data.building_id):
        raise HTTPException(status_code=400, detail="Building does not exist")

    try:
        return create_room(db, room_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Room already exists in this building")


@router.put("/{room_id}", response_model=schemas.RoomRead)
def update_room_route(
    room_id: int,
    room_data: schemas.RoomUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    if room_data.building_id is not None and not get_building_by_id(db, room_data.building_id):
        raise HTTPException(status_code=400, detail="Building does not exist")
    try:
        room = update_room(db, room_id, room_data)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Room update violates uniqueness rules")


@router.delete("/{room_id}")
def delete_room_route(room_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    room = delete_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}
