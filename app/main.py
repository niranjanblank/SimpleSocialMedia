from fastapi import FastAPI
from app.database import create_db_and_tables
from .routers import user_router, board_router, board_list_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# include the routers
app.include_router(user_router.router)
app.include_router(board_router.router)
app.include_router(board_list_router.router)
