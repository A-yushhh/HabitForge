from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.habit import HabitCreate, HabitUpdate
from app.services.auth_service import get_current_user
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.services.streak_service import get_habit_streak
from app.schemas.streak import StreakResponse
from datetime import date
from sqlalchemy import select, func
from datetime import datetime
from zoneinfo import ZoneInfo
from app.schemas.stats import StatsResponse

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
    
    today = datetime.now(ZoneInfo(current_user.timezone)).date()

    local_completed_date = func.date(
        HabitLog.completed_at.op("AT TIME ZONE")(
            current_user.timezone
        )
    )

    existing_log = db.scalar(
        select(HabitLog).where(
            HabitLog.habit_id == habit.id,
            local_completed_date == today,
        )
    )
    if existing_log is not None:
        raise HTTPException(
            status_code=400,
            detail="Habit already completed today",
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

@router.get("/habits/stats",response_model=StatsResponse,)
def get_habit_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    total_habits = db.scalar(
        select(func.count(Habit.id)).where(
            Habit.user_id == current_user.id,
        )
    )
    today=datetime.now(ZoneInfo(current_user.timezone)).date()
    local_completed_date = func.date(
        HabitLog.completed_at.op("AT TIME ZONE")(current_user.timezone)
    )
    completed_today = db.scalar(
        select(func.count(HabitLog.id))
        .join(Habit, Habit.id == HabitLog.habit_id)
        .where(
            Habit.user_id == current_user.id,
            local_completed_date == today,
        )
    )
    habits = db.scalars(
        select(Habit).where(
            Habit.user_id == current_user.id,
        )
    ).all()
    best_streak = 0
    for habit in habits:
        streak = get_habit_streak(
            habit_id=habit.id,
            db=db,
        )
        best_streak = max(
            best_streak,
            streak["longest_streak"],
        )
    return {
        "total_habits": total_habits or 0,
        "completed_today": completed_today or 0,
        "best_streak": best_streak or 0,
    }


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

