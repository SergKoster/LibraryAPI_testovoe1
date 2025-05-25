from typing import Optional

from pydantic import BaseModel


# Создание (POST)
class CreateBook(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int


# Обновление (PATCH/PUT)
class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = None


# Получение (GET) — response
class GetBook(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int

    class Config:
        from_attributes = True
