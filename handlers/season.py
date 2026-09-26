from aiogram import F
from aiogram.types import CallbackQuery

from database import async_session
from models import User, Match
from sqlalchemy import select, func
from keyboards.season import season_keyboard
from data.clubs import club_emoji


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
            select(Match).where(Match.user_id == user_id)
            .order_by(Match.played_at.desc()).limit(5)
        )
        recent = result.scalars().all()

    club_em = club_emoji(user.club)
    line = "━━━━━━━━━━━━━━━━━━━━━━"

    recent_text = ""
    for m in recent:
        emoji = "✅" if m.result in ["win", "ot_win"] else "❌"
        recent_text += f"{emoji} vs {m.opponent}: {m.score_my}:{m.score_opp}\n"
    if not recent_text:
        recent_text = "Матчей пока нет.\n"

    text = (
        f"🏆  СЕЗОН\n"
        f"{line}\n"
        f"{club_em}  «{user.club}»  ({user.league})\n\n"
        f"📖 Глава: {user.chapter}\n"
        f"📅 День сезона: {user.day}\n"
        f"🏒 Матчей сыграно: {total_matches}\n\n"
        f"{line}\n"
        f"📊  СТАТИСТИКА\n"
        f"✅ Побед: {user.wins}\n"
        f"❌ Поражений: {user.losses}\n"
        f"⚡ ОТ-побед: {user.ot_wins}\n"
        f"⚡ ОТ-поражений: {user.ot_losses}\n\n"
        f"{line}\n"
        f"📜  ПОСЛЕДНИЕ 5 МАТЧЕЙ\n"
        f"{recent_text}"
        f"{line}"
    )
    await callback.message.edit_text(text, reply_markup=season_keyboard())
    await callback.answer()


async def season_table(callback: CallbackQuery):
    await callback.answer("📊 Таблица — в разработке", show_alert=True)


async def season_playoff(callback: CallbackQuery):
    await callback.answer("🏆 Плей-офф — в разработке", show_alert=True)


def register_handlers(dp):
    dp.callback_query.register(season_table, F.data == "season_table")
    dp.callback_query.register(season_playoff, F.data == "season_playoff")
