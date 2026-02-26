from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas, database

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post(
    "/",
    response_model=schemas.ReservationResponse,
    summary="Create a reservation",
    description="Creates a new reservation for a user in a room. Checks for conflicts and validates times."
)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(database.get_db)):
    if reservation.end_time <= reservation.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    if reservation.start_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="start_time cannot be in the past")

    user = db.query(models.User).filter(models.User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    room = db.query(models.Room).filter(models.Room.id == reservation.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not room.is_active:
        raise HTTPException(status_code=400, detail="Room is inactive")

    conflict = db.query(models.Reservation).filter(
        models.Reservation.room_id == reservation.room_id,
        models.Reservation.status == "active",
        models.Reservation.start_time < reservation.end_time,
        models.Reservation.end_time > reservation.start_time
    ).first()
    if conflict:
        raise HTTPException(status_code=409, detail="Room is already booked for this time")

    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get(
    "/",
    response_model=list[schemas.ReservationResponse],
    summary="List all reservations",
    description="Returns a list of all reservations"
)
def list_reservations(db: Session = Depends(database.get_db)):
    return db.query(models.Reservation).all()

@router.get(
    "/{reservation_id}",
    response_model=schemas.ReservationResponse,
    summary="Get reservation by ID",
    description="Fetches a single reservation by its ID. Returns 404 if not found"
)
def get_reservation(reservation_id: int, db: Session = Depends(database.get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.post(
    "/{reservation_id}/cancel",
    response_model=schemas.ReservationResponse,
    summary="Cancel reservation",
    description="Cancels an active reservation. Returns 400 if already cancelled."
)
def cancel_reservation(reservation_id: int, db: Session = Depends(database.get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.status == "cancelled":
        raise HTTPException(status_code=400, detail="Reservation is already cancelled")
    reservation.status = "cancelled"
    db.commit()
    db.refresh(reservation)
    return reservation