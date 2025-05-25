from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Reader(Base):
    """Модель читателей"""
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
