from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session
from ..schemas.schemas import UserRead, UserCreate, UserReadWithBoard, Token
from ..crud.user_crud import create_user, get_user_by_id, read_users
from ..database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import authenticate_user, create_access_token

router = APIRouter()


@router.post("/users/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_session)):
    db_user = create_user(db=db, user=user)
    return db_user


@router.get("/users/{user_id}", response_model=UserReadWithBoard)
def read_user_by_id(user_id: int, db: Session = Depends(get_session)):
    db_user = get_user_by_id(db, user_id)
    return db_user


@router.get("/users/", response_model=list[UserRead])
def read_users_endpoint(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(get_session)):
    db_users = read_users(db, skip=skip, limit=limit)
    return db_users

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """
    User login endpoint. Returns a JWT token if the credentials are correct.
    """

    # Authenticate the userr
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}