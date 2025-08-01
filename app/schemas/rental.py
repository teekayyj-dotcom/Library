from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RentalBase(BaseModel):
    book_id: int
    user_id: int
    due_date: datetime

class RentalCreate(RentalBase):
    pass

class RentalReturn(BaseModel):
    rental_id: int

class Rental(RentalBase):
    id: int
    borrowed_date: datetime
    returned_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True

    class Config:
        orm_mode = True
