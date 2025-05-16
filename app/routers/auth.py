# app/routers/auth.py

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.database import get_db
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])
db_dependency = Annotated[Session, Depends(get_db)]


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


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(req: SignupRequest, db: db_dependency):
    # Check for existing user
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_pw = get_password_hash(req.password)
    user = User(email=req.email, hashed_password=hashed_pw, name=req.name)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db.refresh(user)

    return SignupResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )


@router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    # Fetch user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=expires_delta
    )
    expires_at = datetime.now(timezone.utc) + expires_delta
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_at=expires_at
    )
