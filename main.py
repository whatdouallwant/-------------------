from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

SECRET_KEY = "1ferf4tvrr5rf51f51ce51165e6563465tg4fijcu432734lguebd6wxprmvy375nfxhf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7000


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def token_create(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)): 
    user_check = db.query(models.User).filter(models.User.login == form_data.username, models.User.password== form_data.password).fill()
    if not user_check:
        raise HTTPException(status_code=400, detail="Неправильний логін або пароль")
    
    token = token_create(data={"sub": user_check.login})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/books/{author}", response_model= list[schemas.BookDB])
def get_books(author:str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    boo = db.query(models.Book).filter(models.Author.name == author).all()
    if boo:
        return boo
    raise HTTPException(status_code=404, detail="Автора не знайдено")
    

@app.post('/books/add/')
def add_book(new_book: schemas.BookCreate, 
        db: Session = Depends(get_db), 
        token: str = Depends(oauth2_scheme)):
    db_author = db.query(models.Author).filter(models.Author.name == books.author_name).first()
    if not db_author:
        db_author = models.Author(name = books.author_name)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)

    return {'massege': ',ldl'}
    
    db_book = models.Book(title = book.title, pages = book.pages, author_id = author_name.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
@app.delete('/books/')
def delete_book(title: str = Query(min_length=1, max_length=100),
                author: str = Query(min_length=1, max_length=100),
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    
    boo_db = db.query(models.Book).filter(models.Book.title==title, models.Author.name==author).first()
    if boo_db:
        db.delete(boo_db)
        db.commit()





























