from fastapi import FastAPI
from app.routers import expenses, auth

app = FastAPI(
    title="Expense Tracker API",
    description="Manage your personal expenses with JWT-secured endpoints.",
    version="0.1.0",
)

# Mount the auth router under /auth
app.include_router(auth.router)

# Mount the expenses router under /expenses
app.include_router(expenses.router)
