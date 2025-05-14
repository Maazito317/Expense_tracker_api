# app/routers/auth.py

import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.database import get_db
from app.auth import get_password_hash

router = APIRouter()


# Define request/response schemas (to be expanded later)
class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class SignupResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(req: SignupRequest, db: Session = Depends(get_db)):
    # Check for existing user
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password and create user
    hashed_pw = get_password_hash(req.password)
    user = User(email=req.email, password=hashed_pw, name=req.name)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db.refresh(user)

    return SignupResponse(id=user.id, email=user.email, name=user.name, created_at=user.created_at)


@router.post("/login")
async def login(req: LoginRequest):
    """
    ---  
    Placeholder for user login logic.  
    Will verify credentials and return a JWT.
    """
    return {"message": "Login endpoint reached", "email": req.email}
