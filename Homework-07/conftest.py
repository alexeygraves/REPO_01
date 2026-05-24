import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Homework-05"))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


def _make_client():
    # StaticPool — все соединения идут через один объект, иначе :memory: создаёт
    # новую пустую БД на каждый connect() и таблицы пропадают между запросами
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app), engine


@pytest.fixture
def client():
    c, engine = _make_client()
    yield c
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    r = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
