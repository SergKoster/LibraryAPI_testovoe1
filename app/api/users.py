from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.users import GetUser, CreateUser, UpdateUser
from app.crud.users import get_user, get_users, create_user, update_user, delete_user
from app.core.exceptions import NotFoundError, AlreadyExistsError
from app.api.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[GetUser])
def read_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_users(db)


@router.get("/{user_id}", response_model=GetUser)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_user(db, user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=GetUser, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_in: CreateUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_user(db, user_in)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{user_id}", response_model=GetUser)
def update_user_endpoint(user_id: int, user_in: UpdateUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return update_user(db, user_in, user_id)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", response_model=GetUser)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return delete_user(db, user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
