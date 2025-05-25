from datetime import datetime

from typing import Optional

from pydantic import BaseModel


# Создание (POST)
class CreateBorrow(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: Optional[datetime] = None


# Обновление (PATCH/PUT)
class UpdateBorrow(BaseModel):
    book_id: Optional[int] = None
    reader_id: Optional[int] = None
    borrow_date: Optional[datetime] = None
    return_date: Optional[datetime] = None


# Получение (GET) — response
class GetBorrow(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True
