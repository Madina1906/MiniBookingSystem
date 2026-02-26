from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post(
    "/",
    response_model=schemas.RoomResponse,
    summary="Create new room",
    description="Adds a new meeting room to the system"
)
def create_room(room: schemas.RoomCreate, db: Session = Depends(database.get_db)):
    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get(
    "/",
    response_model=list[schemas.RoomResponse],
    summary="List all rooms",
    description="Returns all meeting rooms, active and inactive"
)
def list_rooms(db: Session = Depends(database.get_db)):
    return db.query(models.Room).all()

@router.get(
    "/{room_id}",
    response_model=schemas.RoomResponse,
    summary="Get room by ID",
    description="Fetches a single room by its ID. Returns 404 if not found"
)
def get_room(room_id: int, db: Session = Depends(database.get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room