from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from ..schemas.schemas import UserRead, UserCreate, UserReadWithBoard
from ..crud.user_crud import create_user, get_user_by_id, read_users
from ..database import get_session

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
