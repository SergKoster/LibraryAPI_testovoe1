from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Book(Base):
    """Модель книг"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    copies = Column(Integer, nullable=False, default=1)
    description = Column(String, nullable=True)
