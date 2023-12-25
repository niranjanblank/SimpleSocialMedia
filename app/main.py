from fastapi import FastAPI, Depends
from app.database import get_session, create_db_and_tables
from app.schemas.user_schema import UserRead, UserCreate
from sqlmodel import Session
from app.crud.user_crud import create_user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_session)):
    db_user = create_user(db=db, user=user)
    return db_user
