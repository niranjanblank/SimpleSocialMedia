from sqlmodel import SQLModel, Field, Relationship


class BoardList(SQLModel, table=True):
    __tablename__ = "lists"
    id: int = Field(default=None, primary_key=True)
    title: str
    board_id: int = Field(foreign_key="boards.id")

    # relationship with Board
    board: 'Board' = Relationship(back_populates="board_lists")

    # relationship with list_card
    list_cards: list["BoardList"] = Relationship(back_populates="belongs_to_list", cascade_delete=True)


