from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# ---- 2. Expense Model ---- #
class ExpenseCategory(str, PyEnum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHERS = "Others"


# ---- 2. User Model ---- #
class User(Base):
    __tablename__ = "users"  # Table name in PostgreSQL

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)  # Optional field
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Establish one-to-many relationship with Expense
    expenses = relationship("Expense", back_populates="owner")


# ---- 3. Expense Model ---- #
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)  # e.g., 20.50
    description = Column(Text, nullable=True)  # Optional
    category = Column(Enum(ExpenseCategory), nullable=False)  # Uses the Enum
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # When expense occurred
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # When record was created

    # ForeignKey to link to User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    # Establish many-to-one relationship with User
    owner = relationship("User", back_populates="expenses")
