from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')

engine = create_engine(DB_URL)


def create_db_and_tables():
    # create all tables if they dont exit
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

