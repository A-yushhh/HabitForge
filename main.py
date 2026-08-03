from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.habits import router
from app.database.database import engine


@asynccontextmanager
async def lifespan(app):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("✅ Connected Successfully!")
        print(result.scalar())

    yield

    print("👋 Shutting down HabitForge...")


app = FastAPI(
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "HabitForge API is running."
    }