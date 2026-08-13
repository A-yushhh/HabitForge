from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, oauth2_scheme 
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin
from app.core.security import verify_password

def authenticate_user(
    db: Session,
    login_data: UserLogin,
) -> User | None:
    user = db.scalar(
    select(User).where(User.email == login_data.email)
        )
    if user is None:
        return None
    if not verify_password(
        login_data.password,
        user.password_hash,
    ):
        return None
    return user

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if payload is None:
        return None

    user_id = payload["sub"]

    user = db.scalar(
        select(User).where(User.id == int(user_id))
    )
    if user is None:
        return None
    
    return user

