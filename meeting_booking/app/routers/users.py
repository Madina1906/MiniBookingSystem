from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "/",
    response_model=schemas.UserResponse,
    summary="Create new user",
    description="Creates a new user in the system with full name and phone number"
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get(
    "/",
    response_model=list[schemas.UserResponse],
    summary="List all users",
    description="Returns a list of all registered users"
)
def list_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

@router.get(
    "/{user_id}",
    response_model=schemas.UserResponse,
    summary="Get user by ID",
    description="Fetches a single user by its ID. Returns 404 if not found"
)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user