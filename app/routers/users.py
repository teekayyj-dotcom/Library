from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import User, UserCreate
from app.database import SessionLocal
from app.models import user
from app.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(user.User).offset(skip).limit(limit).all()

@router.post("/", response_model=User)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user with email already exists
    db_user = db.query(user.User).filter(user.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = user.User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is being changed and if it's already taken
    if user_data.email != db_user.email:
        existing_user = db.query(user.User).filter(user.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for key, value in user_data.dict().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
