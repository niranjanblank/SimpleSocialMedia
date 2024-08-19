from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from ..schemas.schemas import BoardRead, BoardCreate, BoardUpdate, BoardReadWithOwner, BoardReadWithListAndCardAndLabels
from ..models.user import User
from ..auth import get_current_active_user
from ..crud.board_crud import create_board, update_board, read_board_by_id, delete_board, read_boards, \
    read_boards_by_owner_id, update_board_background_image
from ..database import get_session
from sqlmodel import Session
from ..models.board import Board
from ..services.s3_service import list_template_images

router = APIRouter()


# current_user authenticates the route, if not authenticated the route doesnt work
@router.post("/boards", response_model=BoardReadWithOwner)
def create_board_endpoint(board: BoardCreate, db: Session = Depends(get_session)):
    db_board = create_board(db, board)
    return db_board


@router.get("/boards/{board_id}", response_model=BoardReadWithOwner)
def read_board_endpoint(board_id: int, db: Session = Depends(get_session)):
    db_board = read_board_by_id(db, board_id)
    return db_board


@router.get("/boards/data/{board_id}", response_model=BoardReadWithListAndCardAndLabels)
def read_board_endpoint(board_id: int, db: Session = Depends(get_session)):
    db_board = read_board_by_id(db, board_id)
    return db_board


@router.put("/boards/{board_id}", response_model=BoardReadWithOwner)
def update_board_endpoint(board_id: int, board: BoardUpdate, db: Session = Depends(get_session)):
    db_board = update_board(db, board_id, board)
    return db_board


@router.put("/boards/update-background/{board_id}", response_model=BoardReadWithOwner)
def update_board_background_image_endpoint(board_id: int,
                                           image: UploadFile = File(...),
                                           db: Session = Depends(get_session)):
    db_board = update_board_background_image(db, board_id, image)
    return db_board


@router.delete("/boards/{board_id}")
def delete_board_endpoint(board_id: int, db: Session = Depends(get_session)):
    result = delete_board(db, board_id)
    return result


@router.get("/boards/", response_model=list[BoardReadWithOwner])
def read_boards_pagination_endpoint(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0),
                                    db: Session = Depends(get_session)):
    result = read_boards(db, skip=skip, limit=limit)
    return result


@router.get("/boards/owner/{owner_id}", response_model=list[BoardRead])
def read_boards_by_owner_id_endpoint(owner_id: int, db: Session = Depends(get_session)):
    result = read_boards_by_owner_id(db, owner_id)
    return result


@router.get("/boards/images/template-images", response_model=list[str])
def get_template_images():
    return list_template_images("boards/template_images/")
