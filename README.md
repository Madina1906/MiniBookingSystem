# Mini Booking System – Meeting Rooms

## Project Description
This is a simple **Meeting Room Booking System** implemented as a REST API using **FastAPI**.  
It allows users to:
- View available meeting rooms
- Create reservations
- Cancel reservations
- View reservation history

The system prevents:
- Double bookings
- Conflicts
- Invalid reservations (past times, end_time ≤ start_time)
- Booking inactive rooms

---

## Technologies / Tools Used
- **Python 3.11+**
- **FastAPI** – REST API framework
- **SQLAlchemy** – ORM for database interactions
- **SQLite** – Database
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation and serialization
- **Swagger / OpenAPI** – Automatic API documentation

---

## How to Run the Project

1. Clone the repository:
```bash
git clone <https://github.com/Madina1906/MiniBookingSystem>
cd MiniBookingSystem/meeting_booking

Create and activate virtual environment:

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / Mac
python -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn main:app --reload

Open Swagger UI in your browser:

http://127.0.0.1:8000/docs
Business Logic
Users

POST /users – create user

GET /users – list users

GET /users/{id} – get user details

Rooms

POST /rooms – create room

GET /rooms – list rooms

GET /rooms/{id} – get room details

Only active rooms can be reserved

Reservations

POST /reservations – create reservation

GET /reservations – list reservations

GET /reservations/{id} – get reservation details

POST /reservations/{id}/cancel – cancel reservation

Validation Rules

end_time must be after start_time

start_time cannot be in the past

Room must be active

No overlapping reservations for the same room

Reservation Status

active – reservation is currently blocking the room

cancelled – frees the room

completed – optional for past reservations

How to Test API

Use Swagger UI at http://127.0.0.1:8000/docs to interactively test endpoints.

Sample JSONs

User Creation:

{
  "full_name": "Alice Johnson",
  "phone": "998901234567"
}

Room Creation:

{
  "name": "Conference Room A",
  "description": "Room with projector",
  "capacity": 10,
  "is_active": true
}

Reservation Creation:

{
  "user_id": 1,
  "room_id": 1,
  "start_time": "2026-02-26T10:00:00",
  "end_time": "2026-02-26T11:00:00"
}

Cancel Reservation:

POST /reservations/1/cancel
Notes

The SQLite database file is booking.db. Deleting it resets all data.

API uses proper HTTP status codes:

200 – success

400 – invalid input

404 – not found

409 – conflict (double booking)

422 – validation error

Swagger UI automatically documents endpoints, input/output models, and example responses.
