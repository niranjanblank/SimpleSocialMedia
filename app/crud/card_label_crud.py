from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.list_card import ListCard
from ..models.board_label import BoardLabel
from ..models.card_label import CardLabelLink
from ..schemas.schemas import CardLabelBase
from sqlalchemy.exc import IntegrityError


def create_card_label_relationship(db: Session, card_label: CardLabelBase):
    try:
        # Check if the card exists
        card_exists = db.exec(select(ListCard).where(ListCard.id == card_label.card_id)).first()
        if not card_exists:
            raise HTTPException(status_code=400, detail=f"Card with id {card_label.card_id} not found")

        # Check if the label exists
        label_exists = db.exec(select(BoardLabel).where(BoardLabel.id == card_label.label_id)).first()
        if not label_exists:
            raise HTTPException(status_code=400, detail=f"Label with id {card_label.label_id} not found")

        # Check if the card-label link already exists
        existing_link = db.exec(select(CardLabelLink).where(
            CardLabelLink.card_id == card_label.card_id,
            CardLabelLink.label_id == card_label.label_id
        )).first()

        if existing_link:
            raise HTTPException(status_code=400, detail="Card-label relationship already exists.")

        # Create the CardLabelLink to establish the relationship
        card_label_link = CardLabelLink(
            card_id=card_label.card_id,
            label_id=card_label.label_id
        )

        db.add(card_label_link)
        db.commit()
        db.refresh(card_label_link)

        return card_label_link
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error: Card-label relationship might already exist.")
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

