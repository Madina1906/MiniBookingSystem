from fastapi import FastAPI
from .database import engine, Base
from app.routers import users, rooms, reservations 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meeting Room Booking API")

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(reservations.router)

from fastapi import Depends
from sqlalchemy.orm import Session
from app import models, database

@app.delete("/reset")
def reset_database(db: Session = Depends(database.get_db)):
    db.query(models.Reservation).delete()
    db.query(models.Room).delete()
    db.query(models.User).delete()
    db.commit()
    return {"message": "Database reset successful"}