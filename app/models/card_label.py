from sqlmodel import SQLModel, Field, Relationship

class CardLabel(SQLModel, table=True):
    __tablename__ = "card_labels"
    id: int = Field(default=None, primary_key=True)
    label_id: int = Field(foreign_key="labels.id")
    card_id: int = Field(foreign_key="list_cards.id")
