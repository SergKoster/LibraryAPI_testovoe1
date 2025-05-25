from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.core.database import Base

class Borrow(Base):
    """Модель книг"""
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
