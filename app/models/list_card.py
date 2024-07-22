from sqlmodel import SQLModel, Field, Relationship

#
# class Board(SQLModel, table=True):
#     __tablename__ = "boards"
#     id: int = Field(default=None, primary_key=True)
#     title: str
#     description: str
#     owner_id: int = Field(foreign_key="users.id")
#
#     # Relationship to User
#     owner: 'User' = Relationship(back_populates="boards")
#
#     # Relationship to BoardList
#     # cascade delete, when a board is deleted, all the lists inside this board will be deleted
#     board_lists: list["BoardList"] = Relationship(back_populates="board", cascade_delete=True)

class ListCard(SQLModel, table=True):
    __tablename__ = "list_cards"
    id: int = Field(default=None, primary_key=True)
    title: str
    desc: str
    list_id : int = Field(foreign_key="lists.id")

    # Relationship to the board_list
    belongs_to_list: 'BoardList' = Relationship(back_populates="list_cards")