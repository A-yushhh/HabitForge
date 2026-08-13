from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.habit import HabitCreate
from app.services.auth_service import get_current_user
from app.models.habit import Habit
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
