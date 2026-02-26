from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ----------------- Users -----------------
class UserCreate(BaseModel):
    """Data required to create a new user"""
    full_name: str = Field(..., description="Full name of the user", example="Alice Johnson")
    phone: str = Field(..., description="User phone number", example="998901234567")

class UserResponse(BaseModel):
    """Represents a user in the meeting booking system"""
    id: int = Field(..., example=1, description="Unique ID of the user")
    full_name: str = Field(..., example="Alice Johnson", description="Full name of the user")
    phone: str = Field(..., example="998901234567", description="Phone number of the user")
    created_at: datetime = Field(..., example="2026-02-26T12:10:52.637037", description="Date and time the user was created")

    class Config:
        orm_mode = True

# ----------------- Rooms -----------------
class RoomCreate(BaseModel):
    """Data required to create a new meeting room"""
    name: str = Field(..., description="Meeting room name", example="Conference Room A")
    description: Optional[str] = Field(None, description="Description of the room", example="Room with projector")
    capacity: int = Field(..., description="Number of people the room can hold", example=10)
    is_active: Optional[bool] = Field(True, description="Is the room active/available?", example=True)

class RoomResponse(BaseModel):
    """Represents a meeting room"""
    id: int = Field(..., example=1, description="Unique ID of the room")
    name: str = Field(..., example="Conference Room A", description="Meeting room name")
    description: Optional[str] = Field(None, example="Room with projector", description="Description of the room")
    capacity: int = Field(..., example=10, description="Room capacity")
    is_active: bool = Field(..., example=True, description="Is the room active/available?")

    class Config:
        orm_mode = True

# ----------------- Reservations -----------------
class ReservationCreate(BaseModel):
    """Data required to create a reservation"""
    user_id: int = Field(..., description="ID of the user making the reservation", example=1)
    room_id: int = Field(..., description="ID of the room to reserve", example=2)
    start_time: datetime = Field(..., description="Reservation start time", example="2026-02-26T10:00:00")
    end_time: datetime = Field(..., description="Reservation end time", example="2026-02-26T11:00:00")

class ReservationResponse(BaseModel):
    """Represents a reservation in the system"""
    id: int = Field(..., example=1, description="Unique ID of the reservation")
    user_id: int = Field(..., example=1, description="ID of the user who made the reservation")
    room_id: int = Field(..., example=2, description="ID of the room reserved")
    start_time: datetime = Field(..., example="2026-02-26T10:00:00", description="Reservation start time")
    end_time: datetime = Field(..., example="2026-02-26T11:00:00", description="Reservation end time")
    status: str = Field(..., example="active", description="Reservation status: active, cancelled, completed")

    class Config:
        orm_mode = True