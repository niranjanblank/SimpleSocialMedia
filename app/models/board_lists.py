from sqlmodel import SQLModel, Field, Relationship


class BoardList(SQLModel, table=True):
    __tablename__ = "lists"
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    board_id: int = Field(foreign_key="boards.id")



