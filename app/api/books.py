from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.books import GetBook, CreateBook, UpdateBook
from app.crud.books import (
    get_books, get_book, create_book, update_book, delete_book
)
from app.core.exceptions import NotFoundError, AlreadyExistsError
from app.api.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/books", tags=["Books"])


# В этой ручке нет jwt проверки, потому что она самая умная
@router.get("/", response_model=list[GetBook])
def read_books(db: Session = Depends(get_db)):
    return get_books(db)


@router.get("/{book_id}", response_model=GetBook)
def read_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_book(db, book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=GetBook, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(book_in: CreateBook, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_book(db, book_in)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{book_id}", response_model=GetBook)
def update_book_endpoint(
    book_id: int,
    book_in: UpdateBook,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_book(db, book_id, book_in)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{book_id}", response_model=GetBook)
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return delete_book(db, book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
