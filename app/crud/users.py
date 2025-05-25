from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.users import User
from app.schemas.users import UpdateUser, GetUser, CreateUser
from app.core.database import is_existing
from app.core.exceptions import NotFoundError, AlreadyExistsError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Хэшируем пароль функция. Берём обычный, возвращаем уже хэшированный.
    Выводим в отдельную функцию, потому что мы - сигма-кодеры"""
    return pwd_context.hash(password)

def get_users(session: Session):
    result = session.execute(select(User))
    return result.scalars().all()
    

def get_user(session: Session, user_id: int):
    user = session.get(User, user_id)

    if user is None:
        raise NotFoundError("User not found")
    
    return user


def create_user(session: Session, user_in: CreateUser):
    hashed_password = hash_password(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)
    
    if is_existing(session, User, email=user_in.email):
            raise AlreadyExistsError("Email already in use")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_in: UpdateUser, user_id: int):
    user = session.get(User, user_id)

    if user is None:
        raise NotFoundError("User not found")
    
    if user_in.email is not None and user_in.email != user.email:
        if is_existing(session, User, email=user_in.email):
            raise AlreadyExistsError("Email already in use")

    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password" and value:
            user.hashed_password = hash_password(value)
        else:
            setattr(user, field, value)

    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    
    if user is None:
        raise NotFoundError("User not found")

    session.delete(user)
    session.commit()
    return user
    

# Аутентификация

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(session: Session, email: str) -> User:
    return session.execute(select(User).where(User.email == email)).scalar_one_or_none()

def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
