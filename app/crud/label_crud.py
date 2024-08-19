from sqlmodel import Session, select
from ..schemas.schemas import LabelCreate
from ..models.board import Board
from ..models.board_label import BoardLabel
from fastapi import HTTPException


def create_label(db: Session, label: LabelCreate):
    # check if the board exists
    board_exists = db.exec(select(Board).where(Board.id == label.board_id)).first() is not None

    if not board_exists:
        raise HTTPException(status_code=404, detail=f'Board with id of {label.board_id} doesn\' exist')

    try:
        db_label = BoardLabel(title=label.title,
                              color=label.color,
                              board_id=label.board_id
                              )
        db.add(db_label)
        db.commit()
        db.refresh(db_label)
        return db_label
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred in label creation: {e}")


def read_label_by_board_id(db: Session, board_id: int):
    # check if the board exists
    # check if the board exists
    board_exists = db.exec(select(Board).where(Board.id == board_id)).first() is not None

    if not board_exists:
        raise HTTPException(status_code=404, detail=f'Board with id of {board_id} doesn\' exist')

    try:
        statement = select(BoardLabel).where(BoardLabel.board_id == board_id)
        label_data = db.exec(statement)
        return label_data
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred while getting Board Lists: {e}")


def delete_label_by_id(db: Session, label_id: int):
    """ Delete label by id"""
    try:
        db_label = db.get(BoardLabel, label_id)
        if not db_label:
            raise HTTPException(status_code=404, detail="Label not found")
        db.delete(db_label)
        db.commit()
        return {"deleted": True}
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in Label deletion: {e}")
