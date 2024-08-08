from fastapi import APIRouter, Depends
from ..schemas.schemas import ListCardRead, ListCardCreate
from sqlmodel import Session
from ..database import get_session
from ..crud.list_card_crud import create_list_card, read_list_card_by_list_id, find_highest_order_card_in_list

router = APIRouter()

@router.post("/list_card", response_model=ListCardRead)
def create_list_card_endpoint(list_card: ListCardCreate, db: Session = Depends(get_session)):
    """ create list card based on data provided at this endpoint"""
    db_list_card = create_list_card(db, list_card)
    return db_list_card

@router.get("/list_card/list/{list_id}", response_model= list[ListCardRead])
def get_list_card_by_list_id_endpoint(list_id: int, db: Session = Depends(get_session)):
    db_list_cards = read_list_card_by_list_id(db, list_id)
    return db_list_cards

@router.get("/list_card/highest_order/{list_id}", response_model=ListCardRead)
def find_highest_order_card_in_list_endpoint(list_id: int, db: Session = Depends(get_session)):
    highest_order_card = find_highest_order_card_in_list(db, list_id)
    return highest_order_card