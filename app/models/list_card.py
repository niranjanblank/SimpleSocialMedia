from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class ListCard(SQLModel, table=True):
    __tablename__ = "list_cards"
    id: int = Field(default=None, primary_key=True)
    title: str
    desc: str
    order: int
    completed: bool = Field(default=False)


    # date attributes
    created_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    list_id : int = Field(foreign_key="lists.id")

    # Relationship to the board_list
    belongs_to_list: 'BoardList' = Relationship(back_populates="list_cards")