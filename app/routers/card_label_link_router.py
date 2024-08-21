from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..schemas.schemas import CardLabelBase
from ..database import get_session
from ..crud.card_label_crud import create_card_label_relationship, delete_card_label_relationship

router = APIRouter()


@router.post("/card-labels", response_model=CardLabelBase)
def create_card_label_relationship_endpoint(card_label: CardLabelBase, db: Session = Depends(get_session)):
    result = create_card_label_relationship(db, card_label)
    return result

@router.delete("/card-labels/{card_id}/{label_id}")
def delete_card_label_relationship_endpoint(card_id: int, label_id: int, db: Session = Depends(get_session)):
    card_label = CardLabelBase(card_id=card_id, label_id=label_id)
    result = delete_card_label_relationship(db, card_label)
    return result