from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.database import get_db
from app.schemas.habit import HabitCreate, HabitUpdate
from app.services.auth_service import get_current_user
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.services.streak_service import get_habit_streak
from app.schemas.streak import StreakResponse

router = APIRouter()


@router.get("/habits")
def get_habits(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    habits = db.scalars(
        select(Habit).where(Habit.user_id == current_user.id)
    ).all()

    return habits

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
        user_id=current_user.id,
        priority=habit.priority,
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

@router.get("/habits/{habit_id}/logs")
def get_habit_logs(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
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

    logs = db.scalars(
        select(HabitLog)
        .where(HabitLog.habit_id == habit_id)
        .order_by(HabitLog.completed_at.desc())
    ).all()

    return logs

@router.put("/habits/{habit_id}")
def update_habit(
    habit_id: int,
    habit_data: HabitUpdate,
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

    update_data = habit_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(habit, field, value)

    db.commit()
    db.refresh(habit)

    return habit

@router.get(
    "/habits/{habit_id}/streak",
    response_model=StreakResponse,
)
def get_streak(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
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
    streak = get_habit_streak(
        habit_id=habit_id,
        db=db,
    )
    return {
        "habit_id": habit_id,
        **streak,
    }

    
@router.patch("/habits/{habit_id}")
def update_habit(
    habit_id: int,
    habit: HabitUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    existing_habit = db.scalar(
        select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
    )
    if existing_habit is None:
        raise HTTPException(
            status_code=404,
            detail="Habit not found",
        )
    updates = habit.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(existing_habit, field, value)
    db.commit()
    db.refresh(existing_habit)

    return existing_habit


@router.delete("/habits/{habit_id}")
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    existing_habit = db.scalar(
        select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
    )
    if existing_habit is None:
        raise HTTPException(
            status_code=404,
            detail="Habit not found",
        )
    db.delete(existing_habit)
    db.commit()
    return {
        "message": "Habit deleted successfully",
    }

