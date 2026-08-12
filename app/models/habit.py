from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func 
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from app.database.database import Base
from app.models.habit.user import User
from app.models.habit_log import HabitLog



class Habit(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )    
    schedule_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    schedule_config: Mapped[dict] = mapped_column(
        sa.JSON,
        nullable=False,
    )
    color: Mapped[str | None] = mapped_column(
        String(7),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        back_populates="habits",
    )

    logs: Mapped[list["HabitLog"]] = relationship(
        back_populates="habit",
        cascade="all, delete-orphan",
    )
