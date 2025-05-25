from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.borrows import GetBorrow, CreateBorrow, UpdateBorrow
from app.crud.borrows import (
    get_borrows, get_borrow, create_borrow, update_borrow, delete_borrow, 
)
from app.core.exceptions import (
    NotFoundError, NoCopiesAvailable, ReaderAlreadyHasThisBook, ReaderLimit
)
from app.api.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/borrows", tags=["Borrows"])


@router.get("/", response_model=list[GetBorrow])
def read_borrows(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_borrows(db)


@router.get("/{borrow_id}", response_model=GetBorrow)
def read_borrow(borrow_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_borrow(db, borrow_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=GetBorrow, status_code=status.HTTP_201_CREATED)
def create_borrow_endpoint(borrow_in: CreateBorrow, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_borrow(db, borrow_in)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NoCopiesAvailable as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ReaderAlreadyHasThisBook as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ReaderLimit as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{borrow_id}", response_model=GetBorrow)
def update_borrow_endpoint(
    borrow_id: int, borrow_in: UpdateBorrow, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_borrow(db, borrow_id, borrow_in)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{borrow_id}", response_model=GetBorrow)
def delete_borrow_endpoint(borrow_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return delete_borrow(db, borrow_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

