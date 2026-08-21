from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog


def calculate_current_streak(completion_dates: list[date]) -> int:
    if not completion_dates:
        return 0

    unique_dates = sorted(set(completion_dates), reverse=True)

    streak = 1

    for i in range(1, len(unique_dates)):
        if unique_dates[i - 1] - unique_dates[i] == timedelta(days=1):
            streak += 1
        else:
            break

    return streak

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

    return calculate_current_streak(completion_dates)
