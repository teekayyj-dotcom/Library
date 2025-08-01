from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.schemas.book import Book, BookCreate
from app.schemas.import_response import ImportResponse
from app.database import SessionLocal
from app.models import book
from app.dependencies import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(book.Book).offset(skip).limit(limit).all()

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(book.Book).filter(book.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/", response_model=Book)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    try:
        db_book = book.Book(
            title=book_data.title,
            author=book_data.author,
            published_year=book_data.published_year,
            quantity=book_data.quantity
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(book.Book).filter(book.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book_data.dict().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(book.Book).filter(book.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.post("/import-csv", response_model=ImportResponse)
async def import_books_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    csv_text = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    total_processed = 0
    successful_imports = 0
    failed_imports = 0
    error_messages = []
    
    try:
        for row in csv_reader:
            total_processed += 1
            try:
                # Check if book already exists
                existing_book = db.query(book.Book).filter(
                    book.Book.title == row['title'],
                    book.Book.author == row['author']
                ).first()
                
                if existing_book:
                    error_messages.append(f"Book already exists: {row['title']} by {row['author']}")
                    failed_imports += 1
                    continue
                
                # Create new book
                new_book = book.Book(
                    title=row['title'].strip(),
                    author=row['author'].strip(),
                    published_year=int(row['published_year']),
                    quantity=int(row['quantity'])
                )
                db.add(new_book)
                successful_imports += 1
                
            except Exception as e:
                error_messages.append(f"Error importing {row.get('title', 'unknown')}: {str(e)}")
                failed_imports += 1
                continue
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ImportResponse(
        total_processed=total_processed,
        successful_imports=successful_imports,
        failed_imports=failed_imports,
        error_messages=error_messages
    )
