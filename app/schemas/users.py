from typing import Optional

from pydantic import BaseModel


# Создание (POST)
class CreateUser(BaseModel):
    email: str
    password: str


# Обновление (PATCH/PUT)
class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


# Получение (GET) — response
class GetUser(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
