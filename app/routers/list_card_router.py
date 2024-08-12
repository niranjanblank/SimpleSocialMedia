from fastapi import APIRouter, Depends
from ..schemas.schemas import ListCardRead, ListCardCreate, ListCardUpdate, ListCardWithList
from sqlmodel import Session
from ..database import get_session
from ..crud.list_card_crud import create_list_card, read_list_card_by_list_id, \
    find_highest_order_card_in_list, update_list_card, delete_card_by_id, read_list_card_by_id

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

@router.get("/list_card/{list_card_id}", response_model= ListCardWithList )
def get_list_card_by_id(list_card_id: int, db: Session = Depends(get_session)):
    db_card = read_list_card_by_id(db, list_card_id)
    return db_card

@router.get("/list_card/highest_order/{list_id}", response_model=ListCardRead)
def find_highest_order_card_in_list_endpoint(list_id: int, db: Session = Depends(get_session)):
    highest_order_card = find_highest_order_card_in_list(db, list_id)
    return highest_order_card

# delete the card
@router.delete("/list_card/{list_card_id}")
def delete_list_card_endpoint(list_card_id: int, db: Session = Depends(get_session)):
    print(f"Deleting card with ID: {list_card_id}")
    result = delete_card_by_id(db,list_card_id)
    print(f"Result: {result}")
    return result


@router.put("/list_card/{list_card_id}")
def update_list_card_endpoint(list_card_id: int, card_update: ListCardUpdate,
                              db: Session = Depends(get_session)):
    db_card = update_list_card(db,list_card_id,card_update)
    return db_card