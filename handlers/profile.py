from aiogram import F
from aiogram.types import CallbackQuery

from database import async_session
from models import User
from sqlalchemy import select
from keyboards.profile import profile_keyboard
from data.clubs import club_emoji


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

    club_em = club_emoji(user.club)
    line = "━━━━━━━━━━━━━━━━━━━━━━"

    text = (
        f"👤  ПРОФИЛЬ\n"
        f"{line}\n"
        f"{club_em}  {user.name}\n"
        f"    ГМ «{user.club}»  ({user.league})\n"
        f"    Возраст: {user.age}\n"
        f"    Уровень ГМ: {user.level}\n"
        f"    Опыт: {user.xp}\n"
        f"{line}\n"
        f"📈  РЕПУТАЦИЯ\n"
        f"    Болельщики:  {stars_repr(user.rep_fans)}\n"
        f"    Пресса:      {stars_repr(user.rep_press)}\n"
        f"    Игроки:      {stars_repr(user.rep_players)}\n"
        f"    Руководство: {stars_repr(user.rep_board)}\n"
        f"{line}\n"
        f"💰  РЕСУРСЫ\n"
        f"    Монеты:   {user.coins}\n"
        f"    Рубины:   {user.rubies}\n"
        f"    Энергия:  {user.energy}/20\n"
        f"    Бюджет:   {user.budget}\n"
        f"{line}\n"
        f"📖  Глава {user.chapter}  •  День {user.day}\n"
        f"🏒  В: {user.wins}  П: {user.losses}\n"
        f"    ОТ: {user.ot_wins}/{user.ot_losses}\n"
        f"{line}"
    )

    await callback.message.edit_text(text, reply_markup=profile_keyboard())
    await callback.answer()


async def profile_achiev(callback: CallbackQuery):
    await callback.answer("🏆 Достижения — в разработке", show_alert=True)


async def profile_journal(callback: CallbackQuery):
    await callback.answer("📜 Журнал — в разработке", show_alert=True)


def register_handlers(dp):
    dp.callback_query.register(profile_achiev, F.data == "profile_achiev")
    dp.callback_query.register(profile_journal, F.data == "profile_journal")
