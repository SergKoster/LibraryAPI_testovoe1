from typing import Optional

from pydantic import BaseModel


# Создание (POST)
class CreateReader(BaseModel):
    name: str
    email: str


# Обновление (PATCH/PUT)
class UpdateReader(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


# Получение (GET) — response
class GetReader(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
