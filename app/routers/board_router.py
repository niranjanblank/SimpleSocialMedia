from fastapi import APIRouter, Depends
from ..schemas.board_schema import BoardRead, BoardCreate, BoardUpdate
from ..crud.board_crud import create_board, update_board, read_board_by_id, delete_board
from ..database import get_session
from sqlmodel import Session
from ..models.board import Board

router = APIRouter()


@router.post("/boards", response_model=BoardRead)
def create_board_endpoint(board: BoardCreate, db: Session = Depends(get_session)):
    db_board = create_board(db, board)
    return db_board


@router.get("/boards/{board_id}", response_model=BoardRead)
def read_board_endpoint(board_id: int, db: Session = Depends(get_session)):
    db_board = read_board_by_id(db, board_id)
    return db_board


@router.put("/boards/{board_id}", response_model=BoardRead)
def update_board_endpoint(board_id: int, board: BoardUpdate, db: Session = Depends(get_session)):
    db_board = update_board(db, board_id, board)
    return db_board


@router.delete("/boards/{board_id}")
def delete_board_endpoint(board_id: int, db: Session = Depends(get_session)):
    result = delete_board(db, board_id)
    return result
