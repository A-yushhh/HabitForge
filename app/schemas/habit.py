from pydantic import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.habit_log import HabitLog


class HabitCreate(BaseModel):
    name: str
    schedule_type: str
    schedule_config: dict
    description: str | None = None
    color: str | None = None

