import sys
import os

from fastapi.testclient import TestClient
import pytest

# Вот эта штучка нужна чтобы pytest не ругался на импорты (в данном случае main)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from main import app

client = TestClient(app)


# Получаем токен для защищённых тестов с этой функцией!
@pytest.fixture
def auth_token():
    # Зарегистрировать пользователя (или обработать конфликт, если уже есть)
    client.post("/auth/register", json={"email": "test2@example.com", "password": "123456"})
    # Залогиниться
    resp = client.post("/auth/login", data={"username": "test2@example.com", "password": "123456"})
    return resp.json()["access_token"]


# Тест создания пользователя
def test_user_create(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
    }
    data = {
        "email":"bebra@dolbik.ru",
        "password":"MegaPassw0rd_2281337"
    }
    resp = client.post("/users/", json=data, headers=headers)
    assert resp.status_code == 201


# Тест создания книги
def test_book_create_all(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
    }
    data = {
        "title":"Bebrium Of Bebras",
        "author":"Sero Kosta",
        "year":1999,
        "isbn":"228-1337",
        "copies":5,
    }
    resp = client.post("/books/", json=data, headers=headers)
    assert resp.status_code == 201


# Тест создания книги без необязательных полей
def test_book_create_without(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
    }
    data = {
        "title":"Bebrium Of Bebras Without ISBN",
        "author":"Sero Kosta",
        "copies":5,
    }
    resp = client.post("/books/", json=data, headers=headers)
    assert resp.status_code == 201


# Тест создания читателя
def test_reader_create(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
    }
    data = {
        "name":"Sero Kostaaaa",
        "email":"Sero@dolbik.ru",
    }
    resp = client.post("/readers/", json=data, headers=headers)
    assert resp.status_code == 201


# Тест создания записи о том, что читатель взял книгу
def test_create_borrow(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    reader_data = {
        "name": "Test Reader",
        "email": "testborrow@example.com"
    }
    r_resp = client.post("/readers/", json=reader_data, headers=headers)
    assert r_resp.status_code == 201
    reader_id = r_resp.json()["id"]

    book_data = {
        "title": "Book for Borrow",
        "author": "Test Author",
        "copies": 3,
        "isbn":"1"
    }
    b_resp = client.post("/books/", json=book_data, headers=headers)
    assert b_resp.status_code == 201
    book_id = b_resp.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_id": reader_id
    }
    borrow_resp = client.post("/borrows/", json=borrow_data, headers=headers)
    assert borrow_resp.status_code == 201, borrow_resp.text


# Тест создания записи о том, что читатель взял книгу, но своя дата
def test_create_borrow_custom_date(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    reader_data = {
        "name": "Test Reader2",
        "email": "testborrow2@example.com"
    }
    r_resp = client.post("/readers/", json=reader_data, headers=headers)
    assert r_resp.status_code == 201
    reader_id = r_resp.json()["id"]

    book_data = {
        "title": "Book for Borrow2",
        "author": "Test Author2",
        "copies": 3,
        "isbn":"2"
    }
    b_resp = client.post("/books/", json=book_data, headers=headers)
    assert b_resp.status_code == 201
    book_id = b_resp.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_id": reader_id,
        "borrow_date": "2025-05-22T18:30:00Z"
    }
    borrow_resp = client.post("/borrows/", json=borrow_data, headers=headers)
    assert borrow_resp.status_code == 201, borrow_resp.text
    borrow_id = borrow_resp.json()["id"]

    borrow_update_data = {
        "borrow_date": "2025-05-23T18:30:00Z"
    }
    borrow_update_resp = client.patch(f"/borrows/{borrow_id}", json=borrow_update_data, headers=headers)
    assert borrow_update_resp.status_code == 200

    borrow_delete_resp = client.delete(f"/borrows/{borrow_id}", headers=headers)
    assert borrow_delete_resp.status_code == 200


def test_reader_update_and_delete(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Создаём читателя
    data = {
        "name": "Reader For Update",
        "email": "update.reader@example.com",
    }
    resp = client.post("/readers/", json=data, headers=headers)
    assert resp.status_code == 201
    reader_id = resp.json()["id"]

    # Обновляем читателя
    update_data = {
        "name": "Updated Reader Name"
    }
    update_resp = client.patch(f"/readers/{reader_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Reader Name"

    # Удаляем читателя
    delete_resp = client.delete(f"/readers/{reader_id}", headers=headers)
    assert delete_resp.status_code == 200


def test_book_update_and_delete(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Создаём книгу
    data = {
        "title": "Book For Update",
        "author": "Book Author",
        "copies": 2,
        "isbn": "book-update-1"
    }
    resp = client.post("/books/", json=data, headers=headers)
    assert resp.status_code == 201
    book_id = resp.json()["id"]

    # Обновляем книгу
    update_data = {
        "title": "Updated Book Title"
    }
    update_resp = client.patch(f"/books/{book_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated Book Title"

    # Удаляем книгу
    delete_resp = client.delete(f"/books/{book_id}", headers=headers)
    assert delete_resp.status_code == 200


def test_user_update_and_delete(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Создаём пользователя
    data = {
        "email": "updateuser@example.com",
        "password": "BebrikBest666"
    }
    resp = client.post("/users/", json=data, headers=headers)
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    # Обновляем пользователя
    update_data = {
        "email": "updateduser@example.com"
    }
    update_resp = client.patch(f"/users/{user_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["email"] == "updateduser@example.com"

    # Удаляем пользователя
    delete_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_resp.status_code == 200


# Чат гпт жоск накидал гигатест
def test_borrow_everything(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. Создаём читателя
    reader_data = {
        "name": "Mega Reader",
        "email": "megareader@example.com"
    }
    r_resp = client.post("/readers/", json=reader_data, headers=headers)
    assert r_resp.status_code == 201, r_resp.text
    reader_id = r_resp.json()["id"]

    # 2. Создаём 4 книги с разными ISBN (3 норм, 1 для проверки лимита)
    books = []
    for i in range(3):
        book_data = {
            "title": f"Book #{i+1}",
            "author": f"Author {i+1}",
            "copies": 5,
            "isbn": f"TEST-ISBN-{i+1}"
        }
        b_resp = client.post("/books/", json=book_data, headers=headers)
        assert b_resp.status_code == 201, b_resp.text
        books.append(b_resp.json()["id"])

    # 3. Создаём 4-ю книгу (для проверки ошибки по лимиту)
    book4_data = {
        "title": "Book #4",
        "author": "Author 4",
        "copies": 1,
        "isbn": "TEST-ISBN-4"
    }
    b4_resp = client.post("/books/", json=book4_data, headers=headers)
    assert b4_resp.status_code == 201, b4_resp.text
    book4_id = b4_resp.json()["id"]

    # 4. Выдаём 3 книги — должно сработать
    borrow_ids = []
    for book_id in books:
        borrow_data = {"book_id": book_id, "reader_id": reader_id}
        resp = client.post("/borrows/", json=borrow_data, headers=headers)
        assert resp.status_code == 201, resp.text
        borrow_ids.append(resp.json()["id"])

    # 5. Пробуем выдать 4-ю книгу (должна быть ошибка лимита)
    borrow4_data = {"book_id": book4_id, "reader_id": reader_id}
    resp4 = client.post("/borrows/", json=borrow4_data, headers=headers)
    assert resp4.status_code == 409, resp4.text
    assert "limit" in resp4.text.lower() or "limit" in resp4.json()["detail"].lower()

    # 6. Возвращаем первые две книги (PATCH — выставляем return_date)
    for borrow_id in borrow_ids[:2]:
        update_data = {"return_date": "2025-06-01T12:00:00Z"}
        patch_resp = client.patch(f"/borrows/{borrow_id}", json=update_data, headers=headers)
        assert patch_resp.status_code == 200, patch_resp.text

    # 7. Теперь можно взять 4-ю книгу — ДОЛЖНО сработать
    resp4_again = client.post("/borrows/", json=borrow4_data, headers=headers)
    assert resp4_again.status_code == 201, resp4_again.text

    # 8. Пробуем взять книгу, которая ещё не возвращена (третью книгу снова) — должна быть ошибка ReaderAlreadyHasThisBook
    borrow_same = {"book_id": books[2], "reader_id": reader_id}
    resp_same = client.post("/borrows/", json=borrow_same, headers=headers)
    assert resp_same.status_code == 409, resp_same.text
    assert "already" in resp_same.text.lower() or "already" in resp_same.json()["detail"].lower()

    # 9. Создаём книгу без копий (copies=0), пытаемся выдать — ошибка NoCopiesAvailable
    book_no_copies = {
        "title": "NoCopies",
        "author": "Nobody",
        "copies": 0,
        "isbn": "NOCOPIES-ISBN"
    }
    bnc_resp = client.post("/books/", json=book_no_copies, headers=headers)
    assert bnc_resp.status_code == 201, bnc_resp.text
    book_no_copies_id = bnc_resp.json()["id"]

    borrow_no_copies = {"book_id": book_no_copies_id, "reader_id": reader_id}
    resp_nocopies = client.post("/borrows/", json=borrow_no_copies, headers=headers)
    assert resp_nocopies.status_code == 409, resp_nocopies.text
    assert "no copies" in resp_nocopies.text.lower() or "no copies" in resp_nocopies.json()["detail"].lower()


# Тест возврата книги 
def test_return_borrow_and_double_return(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. Создаём читателя
    reader_data = {
        "name": "Return Reader",
        "email": "return.reader@example.com"
    }
    r_resp = client.post("/readers/", json=reader_data, headers=headers)
    assert r_resp.status_code == 201, r_resp.text
    reader_id = r_resp.json()["id"]

    # 2. Создаём книгу с одной копией
    book_data = {
        "title": "Returnable Book",
        "author": "Author Return",
        "copies": 1,
        "isbn": "RETURN-ISBN-1"
    }
    b_resp = client.post("/books/", json=book_data, headers=headers)
    assert b_resp.status_code == 201, b_resp.text
    book = b_resp.json()
    book_id = book["id"]
    assert book["copies"] == 1

    # 3. Делаем borrow (copies уменьшится)
    borrow_data = {"book_id": book_id, "reader_id": reader_id}
    borrow_resp = client.post("/borrows/", json=borrow_data, headers=headers)
    assert borrow_resp.status_code == 201, borrow_resp.text
    borrow = borrow_resp.json()
    borrow_id = borrow["id"]

    # Проверяем, что copies стало 0
    b_after_borrow = client.get(f"/books/{book_id}", headers=headers)
    assert b_after_borrow.status_code == 200
    assert b_after_borrow.json()["copies"] == 0

    # 4. Возвращаем книгу
    return_resp = client.patch(
        f"/borrows/{borrow_id}/return",
        json={},  # пустой, вернёт текущую дату
        headers=headers
    )
    assert return_resp.status_code == 200, return_resp.text
    returned = return_resp.json()
    assert returned["return_date"] is not None

    # После возврата copies должно стать 1 снова
    b_after_return = client.get(f"/books/{book_id}", headers=headers)
    assert b_after_return.status_code == 200
    assert b_after_return.json()["copies"] == 1

    # 5. Пробуем вернуть ещё раз — получаем 409 Conflict
    second_return = client.patch(
        f"/borrows/{borrow_id}/return",
        json={},
        headers=headers
    )
    assert second_return.status_code == 409, second_return.text
    # деталь ошибки Optional: 
    # assert "already returned" in second_return.json()["detail"].lower()

