from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.schemas.rental import Rental, RentalCreate, RentalReturn
from app.database import SessionLocal
from app.models import rental, book, user
from app.dependencies import get_db

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"]
)

@router.post("/", response_model=Rental)
def create_rental(rental_data: RentalCreate, db: Session = Depends(get_db)):
    # Check if book exists and is available
    db_book = db.query(book.Book).filter(book.Book.id == rental_data.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # Check if book is available
    if db_book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    if db_book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    # Check if user exists
    db_user = db.query(user.User).filter(user.User.id == rental_data.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create rental record
    db_rental = rental.Rental(
        book_id=rental_data.book_id,
        user_id=rental_data.user_id,
        expected_return_date=rental_data.expected_return_date
    )
    
    # Update book quantity
    db_book.quantity -= 1
    
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

@router.post("/return/{rental_id}")
def return_book(rental_id: int, db: Session = Depends(get_db)):
    db_rental = db.query(rental.Rental).filter(rental.Rental.id == rental_id).first()
    if not db_rental:
        raise HTTPException(status_code=404, detail="Rental record not found")
    if db_rental.is_returned:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Update rental record
    db_rental.is_returned = True
    db_rental.actual_return_date = datetime.utcnow()
    
    # Update book quantity
    db_book = db.query(book.Book).filter(book.Book.id == db_rental.book_id).first()
    db_book.quantity += 1
    
    db.commit()
    db.refresh(db_rental)
    return {"message": "Book returned successfully"}

@router.get("/", response_model=List[Rental])
def get_rentals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(rental.Rental).offset(skip).limit(limit).all()

@router.get("/active", response_model=List[Rental])
def get_active_rentals(db: Session = Depends(get_db)):
    return db.query(rental.Rental).filter(rental.Rental.is_returned == False).all()

@router.get("/user/{user_id}", response_model=List[Rental])
def get_user_rentals(user_id: int, db: Session = Depends(get_db)):
    return db.query(rental.Rental).filter(rental.Rental.user_id == user_id).all()

@router.get("/{rental_id}", response_model=Rental)
def get_rental(rental_id: int, db: Session = Depends(get_db)):
    db_rental = db.query(rental.Rental).filter(rental.Rental.id == rental_id).first()
    if not db_rental:
        raise HTTPException(status_code=404, detail="Rental record not found")
    return db_rental
