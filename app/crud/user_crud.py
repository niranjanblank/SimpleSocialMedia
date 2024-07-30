from sqlmodel import Session, select
from ..schemas.schemas import UserCreate
from app.models.user import User
from fastapi import HTTPException
from ..auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    try:
        # Check if the username already exists
        existing_user = db.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


def get_user_by_id(db: Session, user_id: int):
    try:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def get_user_by_username(db:Session, username: str):
    try:
        user = db.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
def read_users(db: Session, skip: int, limit: int):
    try:
        # statement to select the users based on skip and limit for pagination
        statement = select(User).offset(skip).limit(limit)
        users = db.exec(statement).all()
        return users
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred while getting Users: {e}")
