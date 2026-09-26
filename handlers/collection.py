from aiogram import F
from aiogram.types import CallbackQuery

from services.card_service import get_user_cards, get_user_card_by_id
from keyboards.collection import collection_keyboard, card_detail_keyboard


RARITY_EMOJI = {
    "bronze": "🥉",
    "silver": "🥈",
    "gold": "🥇",
    "elite": "💎",
    "legend": "👑",
    "icon": "🌟",
}

POSITION_EMOJI = {
    "ЦН": "🎯",
    "ЛП": "⚡",
    "ПП": "⚡",
    "З": "🛡",
    "В": "🧤",
}


def format_card_short(card) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    return f"{rarity} {pos} {card.name} ({card.ovr})"


def format_card_full(card) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    pos = POSITION_EMOJI.get(card.position, "🏒")

    text = (
        f"{rarity} {card.name.upper()}\n"
        f"─────────────────────\n"
        f"{pos} {card.position} • {card.age} лет\n"
        f"OVR: {card.ovr}\n"
        f"─────────────────────\n"
        f"⚡ {card.speed}  🎯 {card.shot}  🎩 {card.pass_}\n"
        f"🛡 {card.defense}  💪 {card.physical}\n"
    )

    if card.position == "В":
        text += f"🧤 {card.goalie}\n"

    text += (
        f"─────────────────────\n"
        f"🌍 {card.country}\n"
        f"🏒 {card.league} • 🏛 {card.club}\n"
        f"🎭 Роль: {card.role}\n"
    )

    return text


async def show_collection(callback: CallbackQuery):
    user_id = callback.from_user.id
    cards = await get_user_cards(user_id)

    if not cards:
        await callback.message.edit_text(
            "🃏 КОЛЛЕКЦИЯ\n"
            "─────────────────────\n\n"
            "У тебя пока нет карточек.\n\n"
            "Открой стартовый пак, чтобы получить первых игроков!",
            reply_markup=collection_keyboard([])
        )
        await callback.answer()
        return

    text = (
        "🃏 МОЯ КОЛЛЕКЦИЯ\n"
        "─────────────────────\n"
        f"Всего карточек: {len(cards)}\n\n"
        "Нажми на карточку, чтобы посмотреть детали:"
    )

    await callback.message.edit_text(text, reply_markup=collection_keyboard(cards))
    await callback.answer()


async def show_card_detail(callback: CallbackQuery):
    user_card_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id

    data = await get_user_card_by_id(user_card_id, user_id)

    if not data:
        await callback.answer("Карточка не найдена", show_alert=True)
        return

    card = data["card"]
    user_card = data["user_card"]

    text = format_card_full(card)
    stars = "⭐" * user_card.stars + "☆" * (5 - user_card.stars)
    text += f"\n{stars}\n"

    if user_card.injury_matches > 0:
        text += f"\n🩹 Травма: {user_card.injury_matches} матчей"

    await callback.message.edit_text(
        text,
        reply_markup=card_detail_keyboard(user_card_id)
    )
    await callback.answer()


async def back_to_collection(callback: CallbackQuery):
    await show_collection(callback)


def register_handlers(dp):
    dp.callback_query.register(show_card_detail, F.data.startswith("card_view_"))
    dp.callback_query.register(back_to_collection, F.data == "back_to_collection")
