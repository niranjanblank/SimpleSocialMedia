from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..schemas.user_schema import UserRead, UserCreate
from ..crud.user_crud import create_user, get_user_by_id
from ..database import get_session

router = APIRouter()


@router.post("/users/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_session)):
    db_user = create_user(db=db, user=user)
    return db_user

@router.get("/users/{user_id}", response_model=UserRead)
def read_user_by_id(user_id: int, db: Session = Depends(get_session)):
    db_user = get_user_by_id(db, user_id)
    return db_user