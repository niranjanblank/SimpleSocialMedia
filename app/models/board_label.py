from sqlmodel import SQLModel, Field, Relationship
from .card_label import CardLabelLink

class BoardLabel(SQLModel, table=True):
    __tablename__ = "labels"
    id: int = Field(default=None, primary_key=True)
    title: str
    color: str
    board_id: int = Field(foreign_key="boards.id")

    # Relationship to Board
    # cascade delete, when a board is deleted, all the labels inside this board will be deleted
    board: 'Board' = Relationship(back_populates="board_labels")

    cards: list["ListCard"] = Relationship(back_populates="labels", link_model=CardLabelLink)

