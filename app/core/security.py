from pwdlib import PasswordHash

from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from app.core.config import settings
from app.models.habit.user import User
from fastapi.security import OAuth2PasswordBearer

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

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        return payload
    except JWTError:
        return None