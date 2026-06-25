import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.database import Base, get_db
from app.main import app
from app.models import Job, MatchAnalysis, Resume, User  # noqa: F401


TEST_DATABASE_URL = settings.test_database_url

if not TEST_DATABASE_URL:
    TEST_DATABASE_URL = settings.database_url.rsplit("/", 1)[0] + "/ai_job_tracker_test"


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def unique_email():
    return f"user-{uuid.uuid4().hex}@example.com"


@pytest.fixture
def auth_headers(client, unique_email):
    password = "password123"

    client.post(
        "/api/auth/signup",
        json={
            "email": unique_email,
            "password": password,
            "full_name": "Test User",
        },
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": unique_email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }