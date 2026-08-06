from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User
from app.schemas.user import UserLogin

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