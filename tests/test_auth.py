# tests/test_auth.py

import pytest
from app.models import User


@pytest.mark.parametrize("email,password,name", [
    ("alice@example.com", "password123", "Alice"),
])
def test_signup_creates_user(client, db_session, email, password, name):
    # 1) Call the signup endpoint
    response = client.post(
        "/auth/signup",
        json={"email": email, "password": password, "name": name},
    )
    assert response.status_code == 201

    data = response.json()
    # 2) Response contains the right fields
    assert data["email"] == email
    assert data["name"] == name
    assert "id" in data and isinstance(data["id"], int)
    assert "created_at" in data

    # 3) Verify the user was actually inserted into Postgres
    db_user = db_session.query(User).filter_by(email=email).first()
    assert db_user is not None
    assert db_user.email == email
    assert db_user.name == name
    # Note: hashed_password is stored, not the plaintext
    assert db_user.hashed_password != password


def test_login_returns_jwt_and_expires(client):
    # 1) Sign up a fresh user
    email = "carol@example.com"
    password = "Another$Pass3"
    client.post("/auth/signup", json={"email": email, "password": password})

    # 2) Log in using form data, not JSON
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200

    data = response.json()
    # 3) Check required fields
    assert "access_token" in data
    assert isinstance(data["access_token"], str) and data["access_token"]
    assert data.get("token_type") == "bearer"
    assert "expires_at" in data
