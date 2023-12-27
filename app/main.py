from fastapi import FastAPI, Depends
from app.database import get_session, create_db_and_tables
from .routers import user_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# include the routers
app.include_router(user_router.router)