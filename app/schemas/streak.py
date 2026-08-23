from pydantic import BaseModel


class StreakResponse(BaseModel):
    habit_id: int
    current_streak: int
    longest_streak: int

