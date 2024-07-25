from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session
from ..schemas.schemas import Token
from ..database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import authenticate_user, create_access_token, get_current_active_user,oauth2_scheme


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

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_session)):
    user = await get_current_active_user()
    if user:
        return {"status": "ok"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")