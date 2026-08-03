from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,

        # Temporary
        password_hash=user_data.password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user