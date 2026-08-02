from fastapi import FastAPI
from app.api.habits import router
from sqlalchemy import text
from app.database.database import engine

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("✅ Connected Successfully!")
        print(result.scalar())


@app.get("/")
def root():
    return {
        "message": "HabitForge API is running."
    }

