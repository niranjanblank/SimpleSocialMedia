from fastapi import FastAPI
from app.database import create_db_and_tables
from .routers import user_router, board_router, board_list_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# include the routers
app.include_router(user_router.router)
app.include_router(board_router.router)
app.include_router(board_list_router.router)
