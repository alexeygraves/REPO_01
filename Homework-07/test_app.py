"""
Tests for 5 endpoints of the auth service (Homework-05):
  1. POST /auth/register
  2. POST /auth/login
  3. POST /auth/logout
  4. GET  /students/
  5. POST /students/
"""


# ===================== POST /auth/register =====================

def test_register_success(client):
    r = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "alice123"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data
    # пароль не должен попасть в ответ ни в каком виде
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    payload = {"username": "alice", "email": "alice@example.com", "password": "alice123"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json={**payload, "email": "other@example.com"})
    assert r.status_code == 400
    assert "username" in r.json()["detail"]


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "username": "alice", "email": "shared@example.com", "password": "pass"
    })
    r = client.post("/auth/register", json={
        "username": "bob", "email": "shared@example.com", "password": "pass"
    })
    assert r.status_code == 400
    assert "email" in r.json()["detail"]


# ===================== POST /auth/login =====================

def test_login_success(client):
    client.post("/auth/register", json={
        "username": "alice", "email": "alice@example.com", "password": "alice123"
    })
    r = client.post("/auth/login", data={"username": "alice", "password": "alice123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    # токен не пустой
    assert len(data["access_token"]) > 20


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "alice", "email": "alice@example.com", "password": "alice123"
    })
    r = client.post("/auth/login", data={"username": "alice", "password": "wrong"})
    assert r.status_code == 401


def test_login_nonexistent_user(client):
    r = client.post("/auth/login", data={"username": "nobody", "password": "pass"})
    assert r.status_code == 401


# ===================== POST /auth/logout =====================

def test_logout_returns_200(client):
    r = client.post("/auth/logout")
    assert r.status_code == 200


def test_logout_response_body(client):
    r = client.post("/auth/logout")
    # ответ должен быть json с каким-то сообщением
    assert isinstance(r.json(), dict)
    assert "detail" in r.json() or "message" in r.json()


# ===================== GET /students/ =====================

def test_list_students_requires_auth(client):
    r = client.get("/students/")
    assert r.status_code == 401


def test_list_students_with_token(client, auth_headers):
    r = client.get("/students/", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_list_students_invalid_token(client):
    r = client.get("/students/", headers={"Authorization": "Bearer totally.invalid.token"})
    assert r.status_code == 401


# ===================== POST /students/ =====================

def test_create_student_requires_auth(client):
    r = client.post("/students/", json={"last_name": "Иванов", "first_name": "Иван"})
    assert r.status_code == 401


def test_create_student_success(client, auth_headers):
    r = client.post("/students/",
        json={"last_name": "Иванов", "first_name": "Иван"},
        headers=auth_headers
    )
    assert r.status_code == 201
    data = r.json()
    assert data["last_name"] == "Иванов"
    assert data["first_name"] == "Иван"
    assert "id" in data


def test_created_student_appears_in_list(client, auth_headers):
    client.post("/students/",
        json={"last_name": "Петров", "first_name": "Пётр"},
        headers=auth_headers
    )
    r = client.get("/students/", headers=auth_headers)
    names = [s["last_name"] for s in r.json()]
    assert "Петров" in names
