from sqlalchemy import Column, Integer, String

from app.core.database import Base

class User(Base):
    """Модель библиотекарей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
