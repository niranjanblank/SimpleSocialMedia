from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database import get_session
from ..crud.board_list_crud import create_board_list, get_board_lists_by_board_id
from ..schemas.schemas import BoardListRead, BoardListCreate
router = APIRouter()

@router.post("/board_list", response_model=BoardListRead)
def create_board_list_endpoint(board_list: BoardListCreate, db: Session = Depends(get_session)):
    db_board = create_board_list(db, board_list)
    return db_board

@router.get("/board_list/{board_id}", response_model=list[BoardListRead])
def get_board_lists_by_board_id_endpoint(board_id: int, db: Session = Depends(get_session)):
    db_board_lists = get_board_lists_by_board_id(db, board_id)
    return db_board_lists