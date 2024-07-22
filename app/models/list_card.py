from sqlmodel import SQLModel, Field, Relationship

class ListCard(SQLModel, table=True):
    __tablename__ = "list_cards"
    id: int = Field(default=None, primary_key=True)
    title: str
    desc: str
    list_id : int = Field(foreign_key="lists.id")

    # Relationship to the board_list
    belongs_to_list: 'BoardList' = Relationship(back_populates="list_cards")