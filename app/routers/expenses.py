# app/routers/expenses.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated, List, Literal, Optional
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.auth import get_current_user
from app.database import get_db
from app.models import Expense, ExpenseCategory, User
# from app.auth import get_current_user  # will inject the logged-in user
# from app.database import SessionLocal

router = APIRouter(prefix="/expenses", tags=["Expenses"])
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]
Period = Literal["past_week", "past_month", "past_3_months"]


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
    current_user: user_dependency,
    period: Optional[Period] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    today = date.today()
    if period:
        if period == "past_week":
            start_date = today - timedelta(days=7)
        elif period == "past_month":
            start_date = today - timedelta(days=30)
        elif period == "past_3_months":
            start_date = today - timedelta(days=90)
        end_date = today

    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date cannot be after end_date"
            )

    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    expenses = query.order_by(Expense.date.desc()).all()
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


@router.put("/{expense_id}", response_model=ExpenseOut, status_code=status.HTTP_200_OK)
async def update_expense(expense_id: int, exp_in: ExpenseIn, db: db_dependency, current_user: user_dependency):
    # 1) Fetch the expense, ensure it exists and belongs to this user
    expense = db.query(Expense).get(expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found or not owned by user"
        )

    # 2) Validate category
    try:
        category = ExpenseCategory(exp_in.category)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category: {exp_in.category}"
        )

    # 3) Apply updates
    expense.amount = exp_in.amount
    expense.category = category
    expense.date = exp_in.date
    expense.description = exp_in.description or ""

    # 4) Commit & refresh
    db.commit()
    db.refresh(expense)

    return expense  # Pydantic orm_mode will serialize this


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: db_dependency, current_user: user_dependency):
    # 1) Fetch and authorize
    expense = db.query(Expense).get(expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    # 2) Delete & commit
    db.delete(expense)
    db.commit()
    # 204 response has no body
