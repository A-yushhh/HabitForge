from pydantic import BaseModel


class StatsResponse(BaseModel):
    total_habits: int
    completed_today: int
    best_streak: int