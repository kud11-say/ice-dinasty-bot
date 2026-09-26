from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import async_session
from models import User, UserCard, Card, Match
from sqlalchemy import select, func


def season_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])


async def show_season(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            await callback.answer("Ошибка", show_alert=True)
            return

        result = await session.execute(
            select(func.count(Match.id)).where(Match.user_id == user_id)
        )
        total_matches = result.scalar() or 0

        result = await session.execute(
            select(Match).where(Match.user_id == user_id).order_by(Match.played_at.desc()).limit(5)
        )
        recent = result.scalars().all()

    recent_text = ""
    for m in recent:
        emoji = "✅" if m.result in ["win", "ot_win"] else "❌"
        recent_text += f"{emoji} vs {m.opponent}: {m.score_my}:{m.score_opp}\n"

    if not recent_text:
        recent_text = "Матчей пока нет.\n"

    text = (
        "🏆 СЕЗОН\n─────────────────────\n\n"
        f"📖 Глава: {user.chapter}\n"
        f"📅 День сезона: {user.day}\n"
        f"🏒 Матчей сыграно: {total_matches}\n\n"
        f"📊 СТАТИСТИКА:\n"
        f"✅ Побед: {user.wins}\n"
        f"❌ Поражений: {user.losses}\n"
        f"⚡ ОТ-побед: {user.ot_wins}\n"
        f"⚡ ОТ-поражений: {user.ot_losses}\n\n"
        f"📜 ПОСЛЕДНИЕ 5 МАТЧЕЙ:\n{recent_text}"
    )
    await callback.message.edit_text(text, reply_markup=season_keyboard())
    await callback.answer()


def register_handlers(dp):
    pass
