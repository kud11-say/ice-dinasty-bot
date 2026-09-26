import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# Game
GAME_TIMEZONE = "Europe/Moscow"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в переменных окружения!")
if not ADMIN_ID:
    raise ValueError("ADMIN_ID не задан в переменных окружения!")
