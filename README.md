# Library Management System API

A FastAPI-based Library Management System that allows librarians to manage books, users, and book rentals efficiently.

## Features

- **Book Management**
  - Add, update, delete, and view books
  - Import books from CSV files
  - Track book quantities

- **User Management**
  - Add, update, delete, and view library users
  - Manage user information

- **Rental Management**
  - Handle book borrowing and returns
  - Track rental history
  - Monitor active rentals

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Pydantic

## Project Structure

```
.
├── app/
│   ├── models/         # Database models
│   ├── routers/        # API routes
│   ├── schemas/        # Pydantic models
│   ├── database.py     # Database configuration
│   └── main.py        # FastAPI application
├── test_data/         # Sample data files
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Start the application using Docker:
```bash
docker-compose up --build
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Books
- `GET /api/books` - List all books
- `GET /api/books/{book_id}` - Get book details
- `POST /api/books` - Add new book
- `PUT /api/books/{book_id}` - Update book
- `DELETE /api/books/{book_id}` - Delete book
- `POST /api/books/import-csv` - Import books from CSV

### Users
- `GET /api/users` - List all users
- `GET /api/users/{user_id}` - Get user details
- `POST /api/users` - Add new user
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

### Rentals
- `POST /api/rentals/rent` - Borrow a book
- `POST /api/rentals/return/{rental_id}` - Return a book
- `GET /api/rentals` - List all rentals
- `GET /api/rentals/active` - List active rentals

## License

MIT License