from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()



class Book(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length= 1, max_length= 100)
    pages: int = Field(..., ge=15)



books = {
    "Джордж Оруелл": [
        {"title": "1984", "pages": 328},
        {"title": "Колгосп тварин", "pages": 112}
    ],
    "Стівен Кінг": [
        {"title": "Воно", "pages": 1138},
        {"title": "Сяйво", "pages": 447}
    ],
    "Артур Конан Дойл": [
        {"title": "Пригоди Шерлока Холмса", "pages": 307},
        {"title": "Собака Баскервілів", "pages": 256}
    ],
    "Джоан Роулінг": [
        {"title": "Гаррі Поттер і філософський камінь", "pages": 223},
        {"title": "Гаррі Поттер і таємна кімната", "pages": 251}
    ]
}


@app.get("/books/{author}", response_model= list[schemas.BookDB])
def get_books(author:str, db: Session = Depends(get_db)):
    if author in books:
        boo = db.query(models.Book).filter(models.Author.name == author).all()
        return boo
    
    else:
        return {'message': 'Такого автора не знайдено'}


@app.post('/books/add/')
def add_book(new_book: models.Book):
    if new_book.author not in books:
        books[new_book.author]=[]

    books[new_book.author].append(new_book)

    return {'massege': ',ldl'}
    
    
@app.delete('/books/')
def delete_book(title: str = Query(min_length=1, max_length=100),
                author: str = Query(min_length=1, max_length=100)):
    
    if author in books:
        for book in book[author]:
            if book.title == title:
                books[author].remove(book)
                return{'message': 'Book was deleted'}
