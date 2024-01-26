from sqlmodel import Session, select
from ..schemas.schemas import BoardListCreate
from ..models.board import Board
from ..models.board_lists import BoardList
from fastapi import HTTPException


def create_board_list(db: Session, board_list: BoardListCreate):
    # check if the board exists in the database before adding list to the database
    board_exists = db.exec(select(Board).where(Board.id == board_list.board_id)).first() is not None
    if not board_exists:
        raise HTTPException(status_code=400, detail=f"Board with id of {board_list.board_id} not available")
    try:
        db_board_list = BoardList(title=board_list.title, description=board_list.description,
                                  board_id=board_list.board_id)
        db.add(db_board_list)
        db.commit()
        db.refresh(db_board_list)
        return db_board_list
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred in board creation: {e}")


def get_board_lists(db: Session, skip: int, limit: int):
    try:
        statement = select(BoardList).offset(skip).limit(limit)
        board_list_data = db.exec(statement).all()
        return board_list_data
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred while getting Board Lists: {e}")


def get_board_lists_by_board_id(db: Session, board_id: int):
    """Get all the lists in the current board"""
    # check if the board exists in the database before adding list to the database
    board_exists = db.exec(select(Board).where(Board.id == board_id)).first() is not None
    if not board_exists:
        raise HTTPException(status_code=400, detail=f"Board with id of {board_id} not available")
    try:
        statement = select(BoardList).where(BoardList.board_id == board_id)
        board_list_data = db.exec(statement).all()
        return board_list_data
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred while getting Board Lists: {e}")
