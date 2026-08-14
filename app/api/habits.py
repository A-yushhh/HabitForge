from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.database import get_db
from app.schemas.habit import HabitCreate
from app.services.auth_service import get_current_user
from app.models.habit import Habit
from app.models.habit_log import HabitLog
router = APIRouter()


@router.get("/habits")
def get_habits():
    return {
        "message": "These are all the habits."
    }

@router.post("/habits")
def create_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    ):
    new_habit = Habit(
        name=habit.name,
        description=habit.description,
        schedule_type=habit.schedule_type,
        schedule_config=habit.schedule_config,
        color=habit.color,
        user_id=current_user.id,
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit

@router.post("/habits/{habit_id}/logs")
def complete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    habit = db.scalar(
        select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
    )

    if habit is None:
        raise HTTPException(
            status_code=404,
            detail="Habit not found",
        )

    log = HabitLog(habit_id=habit.id)

    db.add(log)
    db.commit()
    db.refresh(log)

    return log