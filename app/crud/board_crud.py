from sqlmodel import Session, select
from ..schemas.schemas import BoardCreate, BoardUpdate
from ..models.board import Board
from ..models.user import User
from fastapi import HTTPException
def create_board(db: Session, board: BoardCreate):
    # Check if the user exists
    user_exists = db.exec(select(User).where(User.id == board.owner_id)).first() is not None
    if not user_exists:
        raise HTTPException(status_code=400, detail=f"User with id of {board.owner_id} not available")

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
    try:
        db_board = db.get(Board, board_id)
        if not db_board:
            raise HTTPException(status_code=404, detail="Board not found")
        db.delete(db_board)
        db.commit()
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in board deletion: {e}")

def read_boards(db: Session, skip: int, limit: int):
    try:
        # statement to select the users based on skip and limit for pagination
        statement = select(Board).offset(skip).limit(limit)
        boards_data = db.exec(statement).all()
        return boards_data
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as e:
        # Handle unexpected errors
        # Log the error or handle it as needed
        raise HTTPException(status_code=500, detail=f"An error occurred while getting Boards: {e}")
