from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrowed_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime)
    returned_date = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")
