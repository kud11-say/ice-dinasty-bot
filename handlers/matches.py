from aiogram import F
from aiogram.types import CallbackQuery

from database import async_session
from models import User, UserCard, Card, Match
from sqlalchemy import select, func
from services.simulation import get_team_strength, simulate_match
from keyboards.matches import matches_keyboard


OPPONENTS = ["Титаны", "Легион", "Медведи", "Ястребы", "Волки", "Пантеры", "Драконы", "Феникс"]


async def show_matches(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()

    if not user:
        await callback.answer("Ошибка", show_alert=True)
        return

    if user.energy < 3:
        await callback.message.edit_text(
            "⚔️ МАТЧИ\n─────────────────────\n\n"
            f"⚡ Энергия: {user.energy}/20\n\n"
            "Недостаточно энергии для матча (нужно 3).",
            reply_markup=matches_keyboard()
        )
        await callback.answer()
        return

    text = (
        "⚔️ МАТЧИ\n─────────────────────\n\n"
        f"⚡ Энергия: {user.energy}/20\n"
        f"🎮 Матчей сегодня: —\n\n"
        "Сыграть матч против AI-соперника?\n"
        "Стоимость: 3 энергии\n\n"
        "Награда за победу: 1000 монет\n"
        "Награда за поражение: 350 монет"
    )
    await callback.message.edit_text(text, reply_markup=matches_keyboard())
    await callback.answer()


async def play_match(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or user.energy < 3:
            await callback.answer("Недостаточно энергии", show_alert=True)
            return

        # Состав
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id).where(
                UserCard.user_id == user_id, UserCard.is_in_team == True
            )
        )
        team_cards = [{"user_card": uc, "card": c} for uc, c in result.all()]

        if not team_cards:
            await callback.answer("Собери состав!", show_alert=True)
            return

        strength = get_team_strength(team_cards)
        opp = OPPONENTS[func.random()._execute_on_connection] if False else __import__("random").choice(OPPONENTS)
        opp_strength = 65 + __import__("random").randint(-10, 15)

        result_data = simulate_match(strength, opp_strength)

        user.energy -= 3
        if result_data["result"] == "win":
            user.coins += 1000
            user.wins += 1
        elif result_data["result"] == "ot_win":
            user.coins += 800
            user.ot_wins += 1
        elif result_data["result"] == "ot_loss":
            user.coins += 350
            user.ot_losses += 1
        else:
            user.coins += 350
            user.losses += 1

        match = Match(
            user_id=user_id, opponent=opp,
            score_my=result_data["goals_my"], score_opp=result_data["goals_opp"],
            result=result_data["result"]
        )
        session.add(match)
        await session.commit()

    score = f"{result_data['goals_my']}:{result_data['goals_opp']}"
    if result_data["is_ot"]:
        score += " (ОТ)"
    result_ru = {"win": "🏆 ПОБЕДА!", "loss": "😔 ПОРАЖЕНИЕ", "ot_win": "🏆 ПОБЕДА В ОТ!", "ot_loss": "😔 ПОРАЖЕНИЕ В ОТ"}[result_data["result"]]

    text = (
        f"🏒 РЕЗУЛЬТАТ МАТЧА\n─────────────────────\n"
        f"«{user.club}» {score} «{opp}»\n"
        f"{result_ru}\n─────────────────────\n"
        f"📊 xG: {result_data['xg_my']} vs {result_data['xg_opp']}\n"
        f"⚡ Осталось энергии: {user.energy}/20\n\n"
        f"💰 Монеты: {user.coins}"
    )

    from keyboards.matches import after_match_keyboard
    await callback.message.edit_text(text, reply_markup=after_match_keyboard())
    await callback.answer("Матч сыгран!")


def register_handlers(dp):
    dp.callback_query.register(play_match, F.data == "match_play")
