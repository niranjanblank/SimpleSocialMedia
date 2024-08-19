from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING




class Board(SQLModel, table=True):
    __tablename__ = "boards"
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    owner_id: int = Field(foreign_key="users.id")
    background_image_url: str | None = None

    # Relationship to User
    owner: 'User' = Relationship(back_populates="boards")

    # Relationship to BoardList
    # cascade delete, when a board is deleted, all the lists inside this board will be deleted
    board_lists: list["BoardList"] = Relationship(back_populates="board", cascade_delete=True)

    # Relationship to labels
    board_labels: list["BoardLabel"] = Relationship(back_populates="board", cascade_delete=True)
