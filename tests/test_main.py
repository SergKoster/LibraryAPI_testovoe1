import sys
import os

from fastapi.testclient import TestClient
import pytest

# Вот эта штучка нужна чтобы pytest не ругался на импорты (в данном случае main)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from main import app

client = TestClient(app)


def test_register():
    # Регистрация
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "verystrongpassword"
    })
    assert response.status_code == 201, response.text


def test_login():
    response = client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "verystrongpassword"
    })
    assert response.status_code == 200, response.text


def test_books():
    response = client.get("/books/")
    assert response.status_code == 200



