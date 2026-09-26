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
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
    if not user or not user.is_registered:
        await callback.answer("Сначала зарегистрируйся!", show_alert=True)
        return
    text = (
        "╔══════════════════════════╗\n"
        "║  👤 ПРОФИЛЬ ГМ           ║\n"
        "╠══════════════════════════╣\n"
        f"║  {user.name[:22]:<23}║\n"
        f"║  ГМ «{user.club}»{' ' * max(0, 18 - len(user.club))}║\n"
        f"║  Возраст: {user.age:<14}║\n"
        f"║  Уровень ГМ: {user.level:<12}║\n"
        f"║  Опыт: {user.xp:<17}║\n"
        "╠══════════════════════════╣\n"
        "║  📈 РЕПУТАЦИЯ            ║\n"
        f"║  Болельщики:  {stars_repr(user.rep_fans)}║\n"
        f"║  Пресса:      {stars_repr(user.rep_press)}║\n"
        f"║  Игроки:      {stars_repr(user.rep_players)}║\n"
        f"║  Руководство: {stars_repr(user.rep_board)}║\n"
        "╠══════════════════════════╣\n"
        "║  💰 РЕСУРСЫ              ║\n"
        f"║  Монеты: {user.coins:<14}║\n"
        f"║  Рубины: {user.rubies:<14}║\n"
        f"║  Энергия: {user.energy}/20{' ' * 11}║\n"
        f"║  Бюджет: {user.budget:<14}║\n"
        "╠══════════════════════════╣\n"
        f"║  📖 Глава {user.chapter} • День {user.day:<8}║\n"
        f"║  В: {user.wins}  П: {user.losses}{' ' * 14}║\n"
        "╚══════════════════════════╝"
    )
    await callback.message.edit_text(text, reply_markup=profile_keyboard())
    await callback.answer()


def register_handlers(dp):
    pass
