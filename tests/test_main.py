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


def test_protected_endpoint_requires_token():
    # Попытка получить защищённый ресурс без токена
    resp = client.get("/users/")  # любой защищённый роут, например список пользователей
    assert resp.status_code == 401
    # Проверяем, что вернулось правильное сообщение
    assert resp.json()["detail"] == "Could not validate credentials"
    # И заголовок WWW-Authenticate должен присутствовать
    assert "WWW-Authenticate" in resp.headers

