from fastapi import APIRouter, Depends
from ..schemas.schemas import LabelRead, LabelCreate, LabelUpdate
from sqlmodel import Session
from ..database import get_session
from ..crud.label_crud import create_label, read_label_by_board_id, delete_label_by_id, update_label

router = APIRouter()


@router.post("/labels", response_model=LabelRead)
def create_label_endpoint(label: LabelCreate, db: Session = Depends(get_session)):
    result = create_label(db, label)
    return result


@router.get("/boards/{board_id}/labels", response_model=list[LabelRead])
def read_label_by_board_id_endpoint(board_id: int, db: Session = Depends(get_session)):
    result = read_label_by_board_id(db, board_id)
    return result

@router.delete("/labels/{label_id}")
def delete_label_by_id_endpoint(label_id: int,  db: Session = Depends(get_session)):
    result = delete_label_by_id(db, label_id)
    return result

@router.put("/labels/{label_id}")
def update_label_endpoint(label_id: int,label: LabelUpdate, db: Session = Depends(get_session)):
    result = update_label(db, label_id, label)
    return result