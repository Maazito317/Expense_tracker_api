# app/routers/auth.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


# Define request/response schemas (to be expanded later)
class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(req: SignupRequest):
    """
    ---  
    Placeholder for user signup logic.  
    Will validate input, hash password, and create a new user.
    """
    return {"message": "Signup endpoint reached", "email": req.email}


@router.post("/login")
async def login(req: LoginRequest):
    """
    ---  
    Placeholder for user login logic.  
    Will verify credentials and return a JWT.
    """
    return {"message": "Login endpoint reached", "email": req.email}
