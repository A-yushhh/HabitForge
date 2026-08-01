from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
from app.core.config import settings
