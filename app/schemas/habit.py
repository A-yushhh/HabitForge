from pydantic import BaseModel
from typing import Literal
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
    priority: Literal["high", "medium", "low"] | None = None

class HabitUpdate(BaseModel):
    name: str | None = None
    schedule_type: str | None = None
    schedule_config: dict | None = None
    description: str | None = None
    priority: Literal["high", "medium", "low"] = "medium"


