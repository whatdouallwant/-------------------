from pydantic import BaseModel, Field
from typing import List

class Author(BaseModel):
    name: str = Field(..., min_length= 1, max_length= 100)


class Book(BaseModel):

    title: str = Field(..., min_length= 1, max_length= 100)
    pages: int = Field(..., ge=15)


class BookDB(Book):
    id: int
    author: Author
    class Config:
        orm_mode = True


class AuthorDB(Author):
    id: int
    books: List[BookDB]= []
    class Config:
        orm_mode = True