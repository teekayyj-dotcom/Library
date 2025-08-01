from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    published_year: int
    quantity: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
