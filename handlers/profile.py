from aiogram import F
from aiogram.types import CallbackQuery

from database import async_session
from models import User
from sqlalchemy import select
from keyboards.profile import profile_keyboard


def stars_repr(value: int) -> str:
    value = max(0, min(5, value))
    return "⭐" * value + "☆" * (5 - value)


async def show_profile(callback: CallbackQuery):
    user_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

    if not user or not user.is_registered:
        await callback.answer("Сначала зарегистрируйся!", show_alert=True)
        return

    text = (
        "👤 ПРОФИЛЬ\n"
        "─────────────────────\n"
        f"Имя: {user.name}\n"
        f"Клуб: «{user.club}» ({user.league})\n"
        f"Возраст: {user.age}\n"
        f"Уровень ГМ: {user.level}\n"
        f"Опыт: {user.xp}\n"
        "─────────────────────\n"
        "📈 РЕПУТАЦИЯ\n"
        f"Болельщики:  {stars_repr(user.rep_fans)}\n"
        f"Пресса:      {stars_repr(user.rep_press)}\n"
        f"Игроки:      {stars_repr(user.rep_players)}\n"
        f"Руководство: {stars_repr(user.rep_board)}\n"
        "─────────────────────\n"
        "💰 РЕСУРСЫ\n"
        f"Монеты: {user.coins}\n"
        f"Рубины: {user.rubies}\n"
        f"Энергия: {user.energy} / 20\n"
        "─────────────────────\n"
        f"📖 Глава {user.chapter} • День {user.day}"
    )

    await callback.message.edit_text(text, reply_markup=profile_keyboard())
    await callback.answer()


def register_handlers(dp):
    pass
