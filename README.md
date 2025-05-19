# Expense Tracker API

A FastAPI-based backend for tracking personal expenses, secured with JWT authentication and backed by PostgreSQL in Docker.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Setup & Run](#setup--run)  
   - [Environment Variables](#environment-variables)  
   - [Docker Compose](#docker-compose)  
   - [Apply Migrations](#apply-migrations)  
   - [Start the API](#start-the-api)  
4. [Testing](#testing)  
5. [API Usage](#api-usage)  
   - [Interactive Docs](#interactive-docs)  
   - [Auth Endpoints](#auth-endpoints)  
   - [Expenses Endpoints](#expenses-endpoints)  
6. [GitHub Actions CI](#github-actions-ci)  

---

## Features

- **User Authentication**: Signup and login with email + password.  
- **JWT Security**: Issue and verify JWTs for protected routes.  
- **Expense CRUD**: Create, read, update, delete your expenses.  
- **Date Filtering**: List by past week, month, last 3 months or custom date ranges.  
- **Dockerized**: Run PostgreSQL and the API in Docker containers.  
- **Automated Tests**: Pytest suite against a real Postgres instance.  
- **CI**: GitHub Actions workflow to build, migrate, and test on every push.

---

## Prerequisites

- Docker & Docker Compose  
- Python 3.11+ (for local virtualenv & tests)  
- Git  

---

## Setup & Run

### Environment Variables

Create a file named `.env` in the project root:

```env
# PostgreSQL
POSTGRES_USER=tracker_user
POSTGRES_PASSWORD=tracker_password
POSTGRES_DB=tracker_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# JWT settings
SECRET_KEY="a-very-secret-key"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Docker Compose

Build and start the database service:

```bash
docker-compose up -d db
```

This will pull `postgres:15`, create a named volume for data, and expose port `5432` on localhost.

### Apply Migrations

Run Alembic to create the schema:

```bash
docker-compose run --rm web alembic upgrade head
```

*(Use `tester` instead of `web` if you kept a separate migrations service.)*

### Start the API

Bring up the FastAPI service:

```bash
docker-compose up --build web db
```

- The API listens on **http://localhost:8000**  
- Interactive docs at **http://localhost:8000/docs**

---

## Testing

Your tests run against a real Postgres container:

```bash
docker-compose up -d db
pytest -q
```

This will:

1. Recreate the schema  
2. Run signup, login, expense‐CRUD, filtering, and negative‐case tests  

---

## API Usage

### Interactive Docs

Go to **http://localhost:8000/docs** (Swagger UI) to:

- Try **POST /auth/signup**  
- Try **POST /auth/login**  
- Click **Authorize** → paste your Bearer token → test `/expenses` routes

### Auth Endpoints

#### Signup

```http
POST /auth/signup
Content-Type: application/json

{
  "email": "you@example.com",
  "password": "YourPass123",
  "name": "Your Name"
}
```

**Response**: `201 Created`

```json
{
  "id": 1,
  "email": "you@example.com",
  "name": "Your Name",
  "created_at": "2025-05-19T14:30:00Z"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=you@example.com&password=YourPass123
```

**Response**: `200 OK`

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_at": "2025-05-19T15:00:00Z"
}
```

### Expenses Endpoints

> **All `/expenses` routes require**  
> `Authorization: Bearer <jwt>` header

#### Create Expense

```http
POST /expenses/
Content-Type: application/json
Authorization: Bearer <jwt>

{
  "amount": 42.50,
  "category": "Groceries",
  "date": "2025-05-19",
  "description": "Dinner"
}
```

**Response**: `201 Created`

```json
{
  "id": 1,
  "amount": 42.50,
  "category": "Groceries",
  "date": "2025-05-19",
  "description": "Dinner"
}
```

#### List Expenses

```http
GET /expenses/?period=past_week
GET /expenses/?start_date=2025-05-01&end_date=2025-05-10
```

**Response**: `200 OK`  
```json
[
  {
    "id": 1,
    "amount": 42.50,
    "category": "Groceries",
    "date": "2025-05-19",
    "description": "Dinner"
  }
]
```

#### Update Expense

```http
PUT /expenses/{expense_id}
Content-Type: application/json
Authorization: Bearer <jwt>

{
  "amount": 50.00,
  "category": "Utilities",
  "date": "2025-05-18",
  "description": "Electric bill"
}
```

**Response**: `200 OK`

```json
{
  "id": 1,
  "amount": 50.00,
  "category": "Utilities",
  "date": "2025-05-18",
  "description": "Electric bill"
}
```

#### Delete Expense

```http
DELETE /expenses/{expense_id}
Authorization: Bearer <jwt>
```

**Response**: `204 No Content`

---

## GitHub Actions CI

A workflow in `.github/workflows/ci.yml` will:

1. Spin up PostgreSQL 15 service  
2. Install dependencies  
3. Run `alembic upgrade head`  
4. Run `pytest -q`  

Status badge:

```markdown
![CI](https://github.com/<your-org>/Expense_tracker_api/actions/workflows/ci.yml/badge.svg)
```

https://roadmap.sh/projects/expense-tracker-api