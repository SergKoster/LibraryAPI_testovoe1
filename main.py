from fastapi import FastAPI

from app.api import users, books, borrows, readers, auth

app = FastAPI(
    title="SergLibrary API",
    version="1.0.0",
    description="API для Библиотеки"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrows.router)
app.include_router(readers.router)