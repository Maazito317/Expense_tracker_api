from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

from app.database import get_db
from app.models import User

# Load .env file
load_dotenv()

# Read settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# http bearer for jwt
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

db_dependency = Annotated[Session, Depends(get_db)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    :param plain_password: The plain password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    :param password: The password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    :param data: The data to encode in the token.
    :param expires_delta: Optional expiration time delta.
    :return: The encoded JWT token.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    # print(f"ALGORITHM during token creation: {ALGORITHM}")
    # print(f"SECRET_KEY during token decoding: {SECRET_KEY}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: db_dependency,
) -> User:
    # Common 401 exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    decoded_payload = jwt.get_unverified_claims(token)
    print(decoded_payload)
    # Decode & verify the JWT
    try:
        # print("Starting JWT decode")
        # print(f"Token: {token}")
        # print(f"SECRET_KEY: {SECRET_KEY}, ALGORITHM: {ALGORITHM}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        user_id: str = payload.get("user_id")
        if user_id is None:
            # print("User ID not found in token payload.")
            raise credentials_exception
    except JWTError as e:
        # print(f"JWTError: {e}")
        raise credentials_exception

    # 5) Load the user from the DB
    user = db.query(User).get(int(user_id))
    if not user:
        # print("User not found in database.")
        raise credentials_exception

    return user
