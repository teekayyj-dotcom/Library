import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.book import Book
from app.database import Base, DATABASE_URL

# Create engine and tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_books():
    db = SessionLocal()
    try:
        with open('test_data/books.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if book already exists
                existing_book = db.query(Book).filter(
                    Book.title == row['title'],
                    Book.author == row['author']
                ).first()
                
                if existing_book:
                    print(f"Book already exists: {row['title']} by {row['author']}")
                    continue
                
                book = Book(
                    title=row['title'].strip(),
                    author=row['author'].strip(),
                    published_year=int(row['published_year']),
                    quantity=int(row['quantity'])
                )
                db.add(book)
                print(f"Added book: {row['title']} by {row['author']}")
            
            db.commit()
            print("Import completed successfully!")
    except Exception as e:
        print(f"Error during import: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_books()
