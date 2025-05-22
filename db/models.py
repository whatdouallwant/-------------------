from sqlalchemy import Boolean, Column, ForeignKey,Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(99), index=True, nullable=False)

    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(99), index=True, nullable=False)
    pages = Column(Integer)

    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship(Author, back_populates="books")
