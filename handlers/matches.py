import random
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database import async_session
from models import User, UserCard, Card, Match
from sqlalchemy import select
from data.clubs import club_emoji


OPPONENTS = [
    ("Титаны", 78), ("Легион", 74), ("Медведи", 76), ("Ястребы", 72),
    ("Волки", 75), ("Пантеры", 73), ("Драконы", 77), ("Феникс", 71),
]


def _sim_period(attack_a, attack_b, goalie_a, goalie_b, period_num):
    events = []
    goals_a = 0
    goals_b = 0
    shots_a = 0
    shots_b = 0
    for minute in range(1, 21):
        if random.random() < (attack_a / 100) * 0.35:
            shots_a += 1
            if random.random() < 0.14:
                goals_a += 1
                scorers = ["№8", "№17", "№71", "№92", "№10", "№23"]
                events.append(f"⏱ {period_num}:{minute:02d}  🎯 ГОЛ! {random.choice(scorers)}")
        if random.random() < (attack_b / 100) * 0.35:
            shots_b += 1
            if random.random() < 0.13:
                goals_b += 1
                events.append(f"⏱ {period_num}:{minute:02d}  ⚠️ Гол соперника")
        if random.random() < 0.02:
            events.append(f"⏱ {period_num}:{minute:02d}  🟥 Удаление (2 мин)")
    return events, goals_a, goals_b, shots_a, shots_b


async def show_matches(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()

    if not user:
        await callback.answer("Ошибка", show_alert=True)
        return

    club_em = club_emoji(user.club)
    text = (
        f"⚔️ МАТЧ\n"
        f"─────────────────────\n"
        f"{club_em} «{user.club}»\n\n"
        f"⚡ Энергия: {user.energy}/20\n"
        f"💰 Монеты: {user.coins}\n\n"
        "Сыграть товарищеский матч против AI?\n"
        "Стоимость: 3 энергии\n"
        "Награда: 500–1500 монет\n\n"
        "─────────────────────\n"
        "Выбери тактику:"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Атакующая", callback_data="match_tactic_attack")],
        [InlineKeyboardButton(text="🛡 Оборонительная", callback_data="match_tactic_defense")],
        [InlineKeyboardButton(text="💪 Прессинг", callback_data="match_tactic_press")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


async def play_match(callback: CallbackQuery, state: FSMContext):
    tactic = callback.data.replace("match_tactic_", "")
    user_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or user.energy < 3:
            await callback.answer("Недостаточно энергии (нужно 3)", show_alert=True)
            return

        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id).where(
                UserCard.user_id == user_id, UserCard.is_in_team == True
            )
        )
        team = [{"uc": uc, "card": c} for uc, c in result.all()]

        if not team:
            await callback.answer("Собери состав!", show_alert=True)
            return

        forwards = [t for t in team if t["card"].position in ["ЦН", "ЛП", "ПП"]]
        defense = [t for t in team if t["card"].position == "З"]
        goalies = [t for t in team if t["card"].position == "В"]

        attack = sum(c["card"].shot + c["card"].pass_ for c in forwards) / max(len(forwards), 1) / 2
        defense_rating = sum(c["card"].defense for c in defense) / max(len(defense), 1) if defense else 50
        goalie_rating = goalies[0]["card"].goalie if goalies else 50

        if tactic == "attack":
            attack += 10
            defense_rating -= 8
        elif tactic == "defense":
            attack -= 8
            defense_rating += 10
        elif tactic == "press":
            attack += 5
            defense_rating += 3

        attack = max(30, min(99, attack))
        defense_rating = max(30, min(99, defense_rating))

        opp_name, opp_power = random.choice(OPPONENTS)

        # Симуляция по периодам
        p1 = _sim_period(attack, opp_power, goalie_rating, 75, 1)
        p2 = _sim_period(attack, opp_power, goalie_rating, 75, 2)
        p3 = _sim_period(attack, opp_power, goalie_rating, 75, 3)

        goals_my = p1[1] + p2[1] + p3[1]
        goals_opp = p1[2] + p2[2] + p3[2]
        shots_my = p1[3] + p2[3] + p3[3]
        shots_opp = p1[4] + p2[4] + p3[4]

        # Овертайм
        ot = False
        if goals_my == goals_opp:
            ot = True
            if random.random() < 0.5:
                goals_my += 1
            else:
                goals_opp += 1

        # Награды
        if goals_my > goals_opp:
            coins = 1500 if not ot else 1200
            result_str = "win"
            user.wins += 1
        else:
            coins = 500
            result_str = "loss"
            user.losses += 1

        user.energy -= 3
        user.coins += coins

        match = Match(
            user_id=user_id, opponent=opp_name,
            score_my=goals_my, score_opp=goals_opp,
            result=result_str
        )
        session.add(match)
        await session.commit()
        club = user.club

    # Формируем текст матча
    club_em = club_emoji(club)
    text = (
        f"🏒 МАТЧ: «{club}» vs «{opp_name}»\n"
        f"{club_em}\n"
        "═════════════════════\n"
        "1-Й ПЕРИОД\n"
        + ("\n".join(p1[0]) if p1[0] else "  — без голов —") + "\n"
        f"Счёт: {p1[1]}:{p1[2]}\n"
        "═════════════════════\n"
        "2-Й ПЕРИОД\n"
        + ("\n".join(p2[0]) if p2[0] else "  — без голов —") + "\n"
        f"Счёт: {p1[1]+p2[1]}:{p1[2]+p2[2]}\n"
        "═════════════════════\n"
        "3-Й ПЕРИОД\n"
        + ("\n".join(p3[0]) if p3[0] else "  — без голов —") + "\n"
        f"Счёт: {goals_my}:{goals_opp}"
    )
    if ot:
        text += "\n═════════════════════\n⭐ ОВЕРТАЙМ — победитель определён!"

    text += (
        "\n═════════════════════\n"
        f"📊 ИТОГ: {goals_my}:{goals_opp}\n"
        f"xG: {round(shots_my * 0.1, 2)} vs {round(shots_opp * 0.1, 2)}\n"
        f"Броски: {shots_my} vs {shots_opp}\n"
        f"💰 +{coins} монет\n"
        f"⚡ Осталось: {user.energy}/20"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Ещё матч", callback_data="menu_matches")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer("Матч сыгран!")


def register_handlers(dp):
    dp.callback_query.register(play_match, F.data.startswith("match_tactic_"))
