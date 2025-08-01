from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_year = Column(Integer)
    quantity = Column(Integer, default=0)
    
    # Relationships
    rentals = relationship("Rental", back_populates="book")
