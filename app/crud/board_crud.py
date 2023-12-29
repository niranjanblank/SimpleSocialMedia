from sqlmodel import Session
from ..schemas.board_schema import BoardCreate, BoardUpdate
from ..models.board import Board
from fastapi import HTTPException
def create_board(db: Session, board: BoardCreate):
    # setting the owner_id to one currently, later will be replaced by real user id
    try:
        db_board = Board(title=board.title, description=board.description, owner_id=board.owner_id)
        db.add(db_board)
        db.commit()
        db.refresh(db_board)
        return db_board
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred in board creation: {e}")


def read_board_by_id(db: Session, board_id: int):
    try:
        db_board = db.get(Board,board_id)
        if db_board is None:
            raise HTTPException(status_code=404, detail="Board not found")
        return db_board
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred in boards: {e}")



def update_board(db: Session, board_id: int, board: BoardUpdate):
    try:
        db_board = db.get(Board, board_id)
        if db_board is None:
            raise HTTPException(status_code=404, detail="Board not found")
        update_data = board.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_board, key, value)
        db.add(db_board)
        db.commit()
        db.refresh(db_board)
        return db_board
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in boards: {e}")


def delete_board(db: Session, board_id: int):
    return None
