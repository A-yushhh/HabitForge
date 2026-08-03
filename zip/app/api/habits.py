from fastapi import APIRouter

router = APIRouter()


@router.get("/habits")
def get_habits():
    return {
        "message": "These are all the habits."
    }