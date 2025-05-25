from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.engine import create_engine
from sqlalchemy import select

from app.core.config import settings


DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


engine = create_engine(DATABASE_URL, pool_pre_ping=True) 
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)
Base = declarative_base()


def get_db():
    """Получаем сессию для подключения к бд"""
    with SessionLocal() as session:
        yield session


def is_existing(session: Session, model, **kwargs) -> bool:
    """Возвращает True, если значение уже есть в таблице"""
    stmt = select(model).filter_by(**kwargs)
    existing = session.execute(stmt).scalar_one_or_none()
    return existing is not None
