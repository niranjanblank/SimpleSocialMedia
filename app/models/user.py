from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str
    # this is hashed password
    password: str

    # Relationship to Board
    boards: list["Board"] = Relationship(back_populates="owner")

