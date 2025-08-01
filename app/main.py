from fastapi import FastAPI
from app.database import Base, engine
from app.routers import books, users, rentals
from app.models.book import Book
from app.models.user import User
from app.models.rental import Rental

# Create the FastAPI app with title and description
app = FastAPI(
    title="Library Management System",
    description="""
    A Library Management System API that allows:
    - Managing books (add, remove, update, view)
    - Managing users (add, remove, update, view)
    - Managing rentals (borrow books, return books, view history)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include all routers
app.include_router(books.router, prefix="/api", tags=["books"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(rentals.router, prefix="/api", tags=["rentals"])

@app.get("/")
def home():
    return {
        "message": "Welcome to Library Management System API",
        "documentation": "/docs",
        "endpoints": {
            "books": "/api/books",
            "users": "/api/users",
            "rentals": "/api/rentals"
        }
    }

# Create all tables on startup
Base.metadata.create_all(bind=engine)
