from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user

from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/login")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, login_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user)

    return{
        "access_token": token,
        "token_type": "bearer",
    }