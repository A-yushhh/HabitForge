from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.habit import Habit

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id"),
        nullable=False,
        index=True,
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    habit: Mapped["Habit"] = relationship(
        back_populates="logs",
    )