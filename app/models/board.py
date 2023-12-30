from sqlmodel import SQLModel, Field, Relationship


class Board(SQLModel, table=True):
    __tablename__ = "boards"
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    owner_id: int = Field(foreign_key="users.id")

    # Relationship to User
    owner: 'User' = Relationship(back_populates="boards")

