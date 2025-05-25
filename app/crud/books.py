from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.books import Book
from app.schemas.books import UpdateBook, GetBook, CreateBook
from app.core.database import is_existing
from app.core.exceptions import NotFoundError, AlreadyExistsError


def get_books(session: Session):
    result = session.execute(select(Book))
    return result.scalars().all()


def get_book(session: Session, book_id: int):
    book = session.get(Book, book_id)

    if book is None:
        raise NotFoundError("Book not found")
    
    return book


def create_book(session: Session, book_in: CreateBook):
    book = Book(**book_in.model_dump())

    
    if is_existing(session, Book, isbn=book_in.isbn):
        raise AlreadyExistsError("Isbn already exists")
    
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def update_book(session: Session, book_id: int, book_in: UpdateBook):
    book = session.get(Book, book_id)

    if book is None:
        raise NotFoundError("Book not found")
    
    if book_in.isbn is not None and book_in.isbn != book.isbn:
        if is_existing(session, Book, isbn=book_in.isbn):
            raise AlreadyExistsError("Isbn already exists")

    for field, value in book_in.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    session.commit()
    session.refresh(book)
    return book


def delete_book(session: Session, book_id: int):
    book = session.get(Book, book_id)

    if book is None:
        raise NotFoundError("Book not found")

    session.delete(book)
    session.commit()
    return book
