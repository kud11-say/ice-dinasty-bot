from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import logging
import os

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан!")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    """Создаёт таблицы и добавляет недостающие колонки."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Миграции: добавляем отсутствующие колонки
        migrations = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS budget INTEGER DEFAULT 500000",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS wins INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS losses INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS ot_wins INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS ot_losses INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS energy_bought INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS rep_fans INTEGER DEFAULT 3",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS rep_press INTEGER DEFAULT 3",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS rep_players INTEGER DEFAULT 3",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS rep_board INTEGER DEFAULT 3",
            "ALTER TABLE user_cards ADD COLUMN IF NOT EXISTS is_in_team BOOLEAN DEFAULT FALSE",
            "ALTER TABLE user_cards ADD COLUMN IF NOT EXISTS slot VARCHAR(16)",
            "ALTER TABLE user_cards ADD COLUMN IF NOT EXISTS is_captain BOOLEAN DEFAULT FALSE",
            "ALTER TABLE user_cards ADD COLUMN IF NOT EXISTS is_assistant BOOLEAN DEFAULT FALSE",
            "ALTER TABLE user_cards ADD COLUMN IF NOT EXISTS form VARCHAR(8) DEFAULT 'normal'",
            "ALTER TABLE user_cards ADD COLUMN IF NOT EXISTS injury_matches INTEGER DEFAULT 0",
        ]

        for sql in migrations:
            try:
                await conn.execute(text(sql))
            except Exception as e:
                logger.warning(f"⚠️ Миграция пропущена: {e}")

    logger.info("✅ Схема БД проверена и обновлена")
