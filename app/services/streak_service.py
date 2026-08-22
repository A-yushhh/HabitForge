from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.habit_log import HabitLog


def calculate_streaks(
    completion_dates: list[date],
    today: date,
) -> dict:
    if not completion_dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
        }
    unique_dates = sorted(set(completion_dates))
    longest_streak = 1
    current_run = 1
    for i in range(1, len(unique_dates)):
        if unique_dates[i] - unique_dates[i - 1] == timedelta(days=1):
            current_run += 1
        else:
            current_run = 1
        longest_streak = max(longest_streak, current_run)
    latest_date = unique_dates[-1]
    if latest_date < today - timedelta(days=1):
        current_streak = 0
    else:
        current_streak = current_run
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    } 


def get_habit_streak(
    habit_id: int,
    db: Session,
) -> int:
    logs = db.scalars(
        select(HabitLog)
        .where(HabitLog.habit_id == habit_id)
        .order_by(HabitLog.completed_at.desc())
    ).all()

    completion_dates = [
        log.completed_at.date()
        for log in logs
    ]

    return calculate_streaks(
    completion_dates,
    date.today(),
)

