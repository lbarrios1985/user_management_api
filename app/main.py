from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from . import models, schemas, crud
from .database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Management API",
    description="RESTful API for user CRUD operations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED, tags=["Users"], summary="Create a new user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user. Username and email must be unique."""
    logger.info(f"Creating user: {user.username}")
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.UserOut], tags=["Users"], summary="List users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List users with pagination."""
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserOut, tags=["Users"], summary="Get user by ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by their ID."""
    user = crud.get_user(db, user_id)
    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserOut, tags=["Users"], summary="Update user")
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Update user fields. Only provided fields will be updated."""
    logger.info(f"Updating user: {user_id}")
    return crud.update_user(db, user_id, user_update)

@app.delete("/users/{user_id}", response_class=JSONResponse, tags=["Users"], summary="Delete user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    logger.info(f"Deleting user: {user_id}")
    crud.delete_user(db, user_id)
    return {"detail": "User deleted."}
