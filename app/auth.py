from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Optional
from .models.user import User
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
import jwt
from .database import get_session
from .schemas.schemas import TokenData, Token
from fastapi import Request
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# get the data from .env file
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# for handling token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# generate hash of password
def get_password_hash(password: str):
    """
    Hashing a password using bcrypt
    """
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password: str, hashed_password: str):
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password,hashed_password)

def get_user(db_session: Session, username: str):
    """
    Retrieve a user from the database by username
    """
    statement = select(User).where(User.username == username)
    result = db_session.exec(statement)
    return result.first()

def authenticate_user(db_session: Session, username:str, password:str):
    """
    Authenticate a user by username and password
    """
    user = get_user(db_session, username)
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, db_session: Session = Depends(get_session)):
    """
    Get the current user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Try to retrieve the token from the cookies
    token = request.cookies.get('access_token')
    if token is None:
        # Try to retrieve the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(db_session, username=token_data.username)
    # Retrieve the user from the database using the username
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

