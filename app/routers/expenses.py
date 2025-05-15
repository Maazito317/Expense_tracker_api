# app/routers/expenses.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
# from app.auth import get_current_user  # will inject the logged-in user
# from app.database import SessionLocal

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_current_user)],
)


class ExpenseIn(BaseModel):
    amount: float
    category: str
    date: str      # YYYY-MM-DD
    description: str = ""


class ExpenseOut(ExpenseIn):
    id: int


@router.get("/", response_model=List[ExpenseOut])
async def list_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    ---  
    Placeholder for listing expenses.  
    Will query the DB for the current user’s records.
    """
    return []


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExpenseOut)
async def create_expense(exp: ExpenseIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    ---  
    Placeholder for creating an expense.  
    Will insert into the DB and return the new record.
    """
    return {**exp.model_dump(), "id": 1}


@router.put("/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: int, exp: ExpenseIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    ---  
    Placeholder for updating an expense by ID.
    """
    return {**exp.model_dump(), "id": expense_id}


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    ---  
    Placeholder for deleting an expense by ID.
    """
    return
