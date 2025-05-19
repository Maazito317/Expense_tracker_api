# tests/test_expenses.py

import pytest
from datetime import date, timedelta


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


def test_create_expense(client, auth_headers):
    payload = {
        "amount": 100.0,
        "category": "Groceries",
        "date": str(date.today()),
        "description": "Test expense"
    }
    resp = client.post("/expenses/", json=payload, headers=auth_headers)
    assert resp.status_code == 201, resp.text

    data = resp.json()
    assert data["amount"] == payload["amount"]
    assert data["category"] == payload["category"]
    assert data["description"] == payload["description"]
    assert isinstance(data["id"], int)


def test_list_expenses(client, auth_headers):
    resp = client.get("/expenses/", headers=auth_headers)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, list)
    # At least one expense (from test_create_expense)
    assert len(data) >= 1
    first = data[0]
    for field in ("id", "amount", "category", "date"):
        assert field in first


def test_update_expense(client, auth_headers):
    # Create a fresh expense
    create = client.post("/expenses/", json={
        "amount": 50.0,
        "category": "Utilities",
        "date": str(date.today()),
        "description": "Original"
    }, headers=auth_headers)
    eid = create.json()["id"]

    # Update it
    updated = client.put(f"/expenses/{eid}", json={
        "amount": 75.5,
        "category": "Utilities",
        "date": str(date.today()),
        "description": "Updated"
    }, headers=auth_headers)
    assert updated.status_code == 200, updated.text

    data = updated.json()
    assert data["id"] == eid
    assert data["amount"] == 75.5
    assert data["description"] == "Updated"


def test_delete_expense(client, auth_headers):
    # Create another expense
    create = client.post("/expenses/", json={
        "amount": 20.0,
        "category": "Leisure",
        "date": str(date.today()),
        "description": "To be deleted"
    }, headers=auth_headers)
    eid = create.json()["id"]

    # Delete it
    delete = client.delete(f"/expenses/{eid}", headers=auth_headers)
    assert delete.status_code == 204

    # Confirm it's gone
    all_expenses = client.get("/expenses/", headers=auth_headers).json()
    ids = [e["id"] for e in all_expenses]
    assert eid not in ids


def test_filter_expenses_by_period(client, auth_headers):
    # Create one recent and one older expense
    today = date.today()
    old_date = today - timedelta(days=10)
    resp1 = client.post("/expenses/", json={
        "amount": 5.0,
        "category": "Health",
        "date": str(today),
        "description": "Recent"
    }, headers=auth_headers)
    resp2 = client.post("/expenses/", json={
        "amount": 6.0,
        "category": "Health",
        "date": str(old_date),
        "description": "Old"
    }, headers=auth_headers)

    # Filter for past_week (7 days)
    filtered = client.get("/expenses/?period=past_week", headers=auth_headers)
    assert filtered.status_code == 200
    data = filtered.json()
    assert all(
        date.fromisoformat(e["date"]) >= today - timedelta(weeks=1)
        for e in data
    )


def test_filter_expenses_by_custom_range(client, auth_headers):
    # Create one today and one far in the past
    today = date.today()
    far_date = today - timedelta(days=30)
    resp1 = client.post("/expenses/", json={
        "amount": 7.0,
        "category": "Others",
        "date": str(today),
        "description": "In range"
    }, headers=auth_headers)
    resp2 = client.post("/expenses/", json={
        "amount": 8.0,
        "category": "Others",
        "date": str(far_date),
        "description": "Out of range"
    }, headers=auth_headers)

    # Custom filter: only today
    query = f"/expenses/?start_date={today.isoformat()}&end_date={today.isoformat()}"
    filtered = client.get(query, headers=auth_headers)
    assert filtered.status_code == 200
    data = filtered.json()
    # Every returned item must have date == today
    assert all(e["date"] == today.isoformat() for e in data)
