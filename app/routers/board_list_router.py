from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database import get_session
from ..crud.board_list_crud import create_board_list, get_board_lists_by_board_id, delete_board_lists_by_id, \
    update_board_list, find_highest_order_list_in_board
from ..schemas.schemas import BoardListRead, BoardListCreate, BoardListUpdate
router = APIRouter()

@router.post("/board_list", response_model=BoardListRead)
def create_board_list_endpoint(board_list: BoardListCreate, db: Session = Depends(get_session)):
    db_board = create_board_list(db, board_list)
    return db_board

@router.get("/board_list/{board_id}", response_model=list[BoardListRead])
def get_board_lists_by_board_id_endpoint(board_id: int, db: Session = Depends(get_session)):
    db_board_lists = get_board_lists_by_board_id(db, board_id)
    return db_board_lists

@router.delete("/board_list/{board_list_id}")
def delete_board_list_by_id_endpoint(board_list_id:int , db: Session = Depends(get_session)):
    result = delete_board_lists_by_id(db, board_list_id)
    return result

@router.put("/board_list/{board_list_id}")
def update_board_list_endpoint(board_list_id:int, board_list_update: BoardListUpdate,
                               db: Session = Depends(get_session)):
    db_board_list = update_board_list(db,board_list_id, board_list_update)
    return db_board_list

@router.get("/board_list/highest_order/{board_id}", response_model=BoardListRead)
def find_highest_order_list_in_board_endpoint(board_id: int, db: Session = Depends(get_session)):
    highest_order_list = find_highest_order_list_in_board(db, board_id)
    return highest_order_list