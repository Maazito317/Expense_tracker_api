# tests/conftest.py

import os
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.models import Base   # your declarative_base()

# 1) Load .env so we pick up POSTGRES_USER, etc.
load_dotenv()

POSTGRES_USER     = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB       = os.getenv("POSTGRES_DB")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)


# 2) Create a SQLAlchemy engine pointing at your Dockerized Postgres
@pytest.fixture(scope="session")
def engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )


# 3) Drop & recreate all tables once before any tests run
@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):
    # ensure clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # optional teardown:
    Base.metadata.drop_all(bind=engine)


# 4) Provide a DB session for each test
@pytest.fixture
def db_session(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# 5) Override FastAPI’s get_db and give a TestClient that uses it
@pytest.fixture
def client(db_session, monkeypatch):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()  # roll back after each request

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
