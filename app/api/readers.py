from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.readers import GetReader, CreateReader, UpdateReader
from app.schemas.books import GetBook
from app.crud.borrows import get_active_books_by_reader
from app.crud.readers import (
    get_readers, get_reader, create_reader, update_reader, delete_reader
)
from app.core.exceptions import NotFoundError, AlreadyExistsError
from app.api.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("/", response_model=list[GetReader])
def read_readers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_readers(db)


@router.get("/{reader_id}", response_model=GetReader)
def read_reader(reader_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_reader(db, reader_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=GetReader, status_code=status.HTTP_201_CREATED)
def create_reader_endpoint(reader_in: CreateReader, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_reader(db, reader_in)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{reader_id}", response_model=GetReader)
def update_reader_endpoint(
    reader_id: int, reader_in: UpdateReader, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_reader(db, reader_id, reader_in)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{reader_id}", response_model=GetReader)
def delete_reader_endpoint(reader_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return delete_reader(db, reader_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    


@router.get("/{reader_id}/active_books", response_model=list[GetBook])
def get_active_books(reader_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    books = get_active_books_by_reader(db, reader_id)
    return books
