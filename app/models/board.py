from sqlmodel import SQLModel, Field


class Board(SQLModel, table=True):
    __tablename__ = "boards"
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    owner_id: int
