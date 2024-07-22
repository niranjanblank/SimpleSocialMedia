from ..schemas.schemas import ListCardCreate
from sqlmodel import Session,select
from ..models.board_lists import BoardList
from ..models.list_card import ListCard
from fastapi import HTTPException


#  Create card in a list
def create_list_card(db: Session, list_card: ListCardCreate):
    """check if the list already exists in the database before adding card to the list"""
    list_exists = db.exec(select(BoardList).where(BoardList.id == list_card.list_id)).first() is not None
    if not list_exists:
        raise HTTPException(status_code=404, detail=f'List with id of {list_card.list_id} doesn\'t exist')
    try:
        db_list_card = ListCard(title=list_card.title,
                                desc=list_card.desc,
                                list_id=list_card.list_id)
        db.add(db_list_card)
        db.commit()
        db.refresh(db_list_card)
        return db_list_card
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred in board creation: {e}")


# read all the card in a list by list_id
def read_list_card_by_list_id(db:Session, list_id: int):
    # check if the list exists
    list_exists = db.exec(select(BoardList).where(BoardList.id == list_id)).first() is not None

    if not list_exists:
        # if list doesnt exists return error
        raise HTTPException(status_code=404, detail=f"List with id of {list_id} not available")

    try:
        statement= select(ListCard).where(ListCard.list_id == list_id)
        list_card_data = db.exec(statement)
        return list_card_data
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred while getting Board Lists: {e}")


