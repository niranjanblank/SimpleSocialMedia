from sqlmodel import SQLModel, Field, Relationship

class CardLabelLink(SQLModel, table=True):
    __tablename__ = "card_labels"
    label_id: int | None = Field(default=None,foreign_key="labels.id", primary_key=True, ondelete="RESTRICT")
    card_id: int | None  = Field(default=None, foreign_key="list_cards.id", primary_key=True, ondelete="RESTRICT")
