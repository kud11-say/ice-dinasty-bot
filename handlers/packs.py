from aiogram import F
from aiogram.types import CallbackQuery

from services.packs import open_pack, PACKS
from services.card_service import format_card_short
from keyboards.packs import packs_keyboard


async def show_packs(callback: CallbackQuery):
    text = (
        "📦 МАГАЗИН ПАКОВ\n─────────────────────\n\n"
        "🥉 Бронзовый — 1 000 монет (3 карты)\n"
        "🥈 Серебряный — 5 000 монет (5 карт)\n"
        "🥇 Золотой — 15 000 монет (5 карт)\n"
        "💎 Элитный — 50 000 монет (3 карты)\n\n"
        "Выбери пак:"
    )
    await callback.message.edit_text(text, reply_markup=packs_keyboard())
    await callback.answer()


async def buy_pack(callback: CallbackQuery):
    pack_key = callback.data.replace("pack_", "")
    result = await open_pack(callback.from_user.id, pack_key)

    if "error" in result:
        if result["error"] == "not_enough_coins":
            await callback.answer(
                f"Недостаточно монет! Нужно {result['need']}, у тебя {result['have']}",
                show_alert=True
            )
        else:
            await callback.answer("Ошибка", show_alert=True)
        return

    cards = result["cards"]
    pack_name = PACKS[pack_key]["name"]
    cards_text = "\n".join([format_card_short(c) for c in cards])

    await callback.message.edit_text(
        f"📦 {pack_name.upper()} ПАК ОТКРЫТ\n"
        "─────────────────────\n"
        "🎉 Ты получил:\n\n"
        f"{cards_text}\n\n"
        "─────────────────────\n"
        f"💰 Потрачено: {result['price']}",
        reply_markup=packs_keyboard()
    )
    await callback.answer("Пак открыт!")


def register_handlers(dp):
    dp.callback_query.register(show_packs, F.data == "menu_packs_alt")
    dp.callback_query.register(buy_pack, F.data.startswith("pack_"))
