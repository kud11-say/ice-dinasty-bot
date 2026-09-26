from aiogram import F
from aiogram.types import CallbackQuery

from database import async_session
from models import UserCard, Card
from sqlalchemy import select
from keyboards.team import team_keyboard, team_empty_keyboard
from services.card_service import format_card_short


SLOT_NAMES = {
    "line1_c": "Звено 1 • ЦН",
    "line1_lw": "Звено 1 • ЛП",
    "line1_rw": "Звено 1 • ПП",
    "line2_c": "Звено 2 • ЦН",
    "line2_lw": "Звено 2 • ЛП",
    "line2_rw": "Звено 2 • ПП",
    "pair1_ld": "Пара 1 • ЛЗ",
    "pair1_rd": "Пара 1 • ПЗ",
    "goalie1": "Вратарь 1",
}

SLOTS_BY_POSITION = {
    "ЦН": ["line1_c", "line2_c"],
    "ЛП": ["line1_lw", "line2_lw"],
    "ПП": ["line1_rw", "line2_rw"],
    "З":  ["pair1_ld", "pair1_rd"],
    "В":  ["goalie1"],
}


async def show_team(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id)
            .where(UserCard.user_id == callback.from_user.id, UserCard.is_in_team == True)
        )
        rows = result.all()

    if not rows:
        await callback.message.edit_text(
            "🏒  МОЙ СОСТАВ\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Состав пуст.\n\n"
            "Открой коллекцию и добавь "
            "игроков в состав.",
            reply_markup=team_empty_keyboard()
        )
        await callback.answer()
        return

    by_slot = {uc.slot: (uc, c) for uc, c in rows if uc.slot}

    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = f"🏒  МОЙ СОСТАВ\n{line}\n"

    for slot_key, slot_name in SLOT_NAMES.items():
        if slot_key in by_slot:
            uc, card = by_slot[slot_key]
            cap = " 👑" if uc.is_captain else (" 🅰️" if uc.is_assistant else "")
            text += f"{slot_name}: {format_card_short(card)}{cap}\n"
        else:
            text += f"{slot_name}: —\n"

    total_ovr = sum(c.ovr for _, c in rows) // len(rows) if rows else 0
    text += (
        f"{line}\n"
        f"Средний OVR: {total_ovr}\n"
        f"Состав: {len(rows)}/9"
    )

    await callback.message.edit_text(text, reply_markup=team_keyboard())
    await callback.answer()


async def add_to_team(callback: CallbackQuery):
    user_card_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id)
            .where(UserCard.id == user_card_id, UserCard.user_id == user_id)
        )
        row = result.first()
        if not row:
            await callback.answer("Не найдено", show_alert=True)
            return

        uc, card = row
        if uc.is_in_team:
            await callback.answer("Уже в составе", show_alert=True)
            return

        result = await session.execute(
            select(UserCard.slot).where(
                UserCard.user_id == user_id, UserCard.is_in_team == True
            )
        )
        used_slots = {r[0] for r in result.all() if r[0]}

        slots = SLOTS_BY_POSITION.get(card.position, [])
        free_slot = None
        for s in slots:
            if s not in used_slots:
                free_slot = s
                break

        if not free_slot:
            await callback.answer(
                f"Нет свободного слота для {card.position}",
                show_alert=True
            )
            return

        uc.is_in_team = True
        uc.slot = free_slot
        await session.commit()

    from handlers.collection import show_card_detail
    await show_card_detail(callback)


async def remove_from_team(callback: CallbackQuery):
    user_card_id = int(callback.data.split("_")[3])
    async with async_session() as session:
        result = await session.execute(
            select(UserCard).where(
                UserCard.id == user_card_id,
                UserCard.user_id == callback.from_user.id
            )
        )
        uc = result.scalar_one_or_none()
        if uc:
            uc.is_in_team = False
            uc.slot = None
            uc.is_captain = False
            uc.is_assistant = False
            await session.commit()

    from handlers.collection import show_card_detail
    await show_card_detail(callback)


async def auto_team(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id)
            .where(UserCard.user_id == user_id).order_by(Card.ovr.desc())
        )
        rows = result.all()

        for uc, _ in rows:
            uc.is_in_team = False
            uc.slot = None

        used = set()
        for uc, card in rows:
            slots = SLOTS_BY_POSITION.get(card.position, [])
            for s in slots:
                if s not in used:
                    uc.is_in_team = True
                    uc.slot = s
                    used.add(s)
                    break

        await session.commit()

    await show_team(callback)


def register_handlers(dp):
    dp.callback_query.register(add_to_team, F.data.startswith("card_to_team_"))
    dp.callback_query.register(remove_from_team, F.data.startswith("card_from_team_"))
    dp.callback_query.register(auto_team, F.data == "team_auto")
