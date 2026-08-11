from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.habit import HabitCreate


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
):
    ...