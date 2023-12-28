from sqlmodel import Session
from ..schemas.board_schema import BoardCreate, BoardUpdate


def create_board(db: Session, board: BoardCreate):
    # setting the owner_id to one currently, later will be replaced by real user id
    owner_id = 1
    return None


def read_board_by_id(db: Session, board_id: int):
    return None


def update_board(db: Session, board_id: int, board: BoardUpdate):
    return None


def delete_board(db: Session, board_id: int):
    return None
