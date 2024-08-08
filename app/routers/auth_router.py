from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session
from ..schemas.schemas import Token
from ..database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import authenticate_user, create_access_token, get_current_active_user,oauth2_scheme
from typing import Annotated
from ..models.user import User
router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """
    User login endpoint. Returns a JWT token if the credentials are correct.
    """

    # Authenticate the userr
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-token")
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"status": "ok", "username": current_user.username, "user_id": current_user.id}