from pwdlib import PasswordHash

from datetime import datetime, timedelta, UTC
from jose import jwt
from app.core.config import settings
from app.models.user import User

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    return password_hasher.verify(
        password,
        hashed_password,
    )

def create_access_token(user: User) -> str:
    payload = {
    "sub": str(user.id),
    "exp": datetime.now(UTC) + timedelta(minutes=30),
    }

    token=jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token

