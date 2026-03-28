"""測試共用 fixtures。"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base, get_db
from src.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=engine)


def override_get_db():
    """測試用的資料庫 session。"""
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    """每個測試前重建資料表。"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """建立測試用 HTTP client。"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db():
    """建立測試用資料庫 session。"""
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
