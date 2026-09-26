from aiogram import F
from aiogram.types import CallbackQuery

from services.card_service import (
    get_user_cards, get_user_card_by_id, format_card_full
)
from keyboards.collection import (
    collection_keyboard, card_detail_keyboard, empty_collection_keyboard
)


async def show_collection(callback: CallbackQuery):
    cards = await get_user_cards(callback.from_user.id)

    if not cards:
        await callback.message.edit_text(
            "🃏  КОЛЛЕКЦИЯ\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "У тебя пока нет карточек.\n\n"
            "Открой стартовый пак, "
            "чтобы получить первых игроков!",
            reply_markup=empty_collection_keyboard()
        )
        await callback.answer()
        return

    text = (
        "🃏  МОЯ КОЛЛЕКЦИЯ\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Всего карточек: {len(cards)}\n\n"
        "Нажми на карточку, чтобы посмотреть детали:"
    )

    await callback.message.edit_text(text, reply_markup=collection_keyboard(cards))
    await callback.answer()


async def show_card_detail(callback: CallbackQuery):
    user_card_id = int(callback.data.split("_")[2])
    data = await get_user_card_by_id(user_card_id, callback.from_user.id)

    if not data:
        await callback.answer("Карточка не найдена", show_alert=True)
        return

    uc = data["user_card"]
    text = format_card_full(data["card"], uc.stars, uc.form, uc.injury_matches)

    await callback.message.edit_text(
        text,
        reply_markup=card_detail_keyboard(user_card_id, uc.is_in_team)
    )
    await callback.answer()


async def back_to_collection(callback: CallbackQuery):
    await show_collection(callback)


def register_handlers(dp):
    dp.callback_query.register(show_card_detail, F.data.startswith("card_view_"))
    dp.callback_query.register(back_to_collection, F.data == "back_to_collection")
