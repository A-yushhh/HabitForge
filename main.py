from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.habits import router
from app.api.users import router as user_router
from app.api.auth import router as auth_router

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
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "HabitForge API is running."
    }