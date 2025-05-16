# app/routers/expenses.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from datetime import date

from app.auth import get_current_user
from app.database import get_db
from app.models import Expense, ExpenseCategory, User
# from app.auth import get_current_user  # will inject the logged-in user
# from app.database import SessionLocal

router = APIRouter(prefix="/expenses", tags=["Expenses"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]


class ExpenseIn(BaseModel):
    amount: float
    category: str
    date: str      # YYYY-MM-DD
    description: str = ""


class ExpenseOut(ExpenseIn):
    id: int
    amount: float
    category: str
    date: date
    description: Optional[str] = None

    class Config:
        orm_mode = True


@router.get(
    "/",
    response_model=List[ExpenseOut]
)
async def list_expenses(
    db: db_dependency,
    current_user: user_dependency
):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseOut
)
async def create_expense(
    exp_in: ExpenseIn,
    db: db_dependency,
    current_user: user_dependency
):
    # Validate the category
    try:
        category = ExpenseCategory(exp_in.category)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category: {exp_in.category}"
        )

    # Build the expense object
    expense = Expense(
        user_id=current_user.id,
        amount=exp_in.amount,
        category=category,
        date=exp_in.date,
        description=exp_in.description or ""
    )
    db.add(expense)

    # Commit and refresh to populate the ID
    db.commit()
    db.refresh(expense)
    return ExpenseOut(
        id=expense.id,
        amount=float(expense.amount),
        category=expense.category.value,
        date=expense.date,
        description=expense.description
    )


@router.put("/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: int, exp: ExpenseIn, db: db_dependency, current_user: user_dependency):
    """
    ---  
    Placeholder for updating an expense by ID.
    """
    return {**exp.model_dump(), "id": expense_id}


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: db_dependency, current_user: user_dependency):
    """
    ---  
    Placeholder for deleting an expense by ID.
    """
    return
