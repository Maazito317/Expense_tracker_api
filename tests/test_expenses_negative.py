# in tests/test_expenses_negative.py
import pytest


@pytest.fixture
def auth_headers(client):
    # Sign up & log in to get a JWT for “dave@example.com”
    email = "dave@example.com"
    password = "Password!4"
    client.post("/auth/signup", json={"email": email, "password": password})
    login_resp = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_expenses_unauthorized(client):
    resp = client.get("/expenses/")
    assert resp.status_code == 401


def test_post_expenses_unauthorized(client):
    resp = client.post("/expenses/", json={
        "amount": 10.0, "category": "Groceries", "date": "2025-05-15"
    })
    assert resp.status_code == 401


def test_create_expense_invalid_category(client, auth_headers):
    resp = client.post("/expenses/", json={
        "amount": 20.0,
        "category": "NotACategory",
        "date": "2025-05-15"
    }, headers=auth_headers)
    assert resp.status_code == 400
    assert "Invalid category" in resp.json()["detail"]

def test_create_expense_missing_fields(client, auth_headers):
    resp = client.post("/expenses/", json={}, headers=auth_headers)
    assert resp.status_code == 422
    errors = resp.json()["detail"]
    # There should be errors mentioning "amount", "category", and "date"
    missing = {e["loc"][-1] for e in errors}
    assert {"amount", "category", "date"}.issubset(missing)
