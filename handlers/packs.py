import asyncio
from aiogram import F
from aiogram.types import CallbackQuery

from services.packs import open_pack, PACKS
from services.card_service import format_card_short
from keyboards.packs import packs_keyboard, after_pack_keyboard


# Анимация прогресса открытия пака
PROGRESS_STEPS = [
    "▓░░░░░░░░░░  10%",
    "▓▓▓░░░░░░░░  30%",
    "▓▓▓▓▓░░░░░░  50%",
    "▓▓▓▓▓▓▓░░░░  70%",
    "▓▓▓▓▓▓▓▓▓░░  90%",
    "▓▓▓▓▓▓▓▓▓▓▓  100%",
]


async def show_packs(callback: CallbackQuery):
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        "🛒  МАГАЗИН ПАКОВ\n"
        f"{line}\n\n"
        "🥉 Бронзовый   — 1 000   (3 карты)\n"
        "🥈 Серебряный  — 5 000   (5 карт)\n"
        "🥇 Золотой     — 15 000  (5 карт)\n"
        "💎 Элитный     — 50 000  (3 карты)\n\n"
        f"{line}\n"
        "Выбери пак:"
    )
    await callback.message.edit_text(text, reply_markup=packs_keyboard())
    await callback.answer()


async def buy_pack(callback: CallbackQuery):
    pack_key = callback.data.replace("pack_", "")
    pack = PACKS.get(pack_key)
    if not pack:
        await callback.answer("Неизвестный пак", show_alert=True)
        return

    user_id = callback.from_user.id
    emoji = pack["emoji"]
    name = pack["name"]

    # Проверяем баланс заранее — чтобы не проигрывать анимацию зря
    from database import async_session
    from models import User
    from sqlalchemy import select
    async with async_session() as session:
        r = await session.execute(select(User).where(User.id == user_id))
        u = r.scalar_one_or_none()

    if not u:
        await callback.answer("Ошибка пользователя", show_alert=True)
        return
    if u.coins < pack["price"]:
        need = pack["price"] - u.coins
        await callback.answer(
            f"Не хватает {need} монет!\nНужно: {pack['price']}, у тебя: {u.coins}",
            show_alert=True
        )
        return

    # ─── Анимация открытия ────────────────────
    msg = callback.message
    header = f"{emoji}  ОТКРЫВАЕМ {name.upper()} ПАК\n━━━━━━━━━━━━━━━━━━━━━━\n"
    try:
        await msg.edit_text(header + "\n▓░░░░░░░░░░  0%")
    except Exception:
        msg = await msg.answer(header + "\n▓░░░░░░░░░░  0%")

    for step in PROGRESS_STEPS:
        await asyncio.sleep(0.4)
        try:
            await msg.edit_text(header + f"\n{step}")
        except Exception:
            pass

    # ─── Открываем пак ──────────────────────
    result = await open_pack(user_id, pack_key)

    if "error" in result:
        await callback.answer("Ошибка открытия", show_alert=True)
        return

    cards = result["cards"]

    # ─── Показываем карты по одной ───────────
    await asyncio.sleep(0.3)
    intro = (
        f"{emoji}  {name.upper()} ПАК ОТКРЫТ!\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎉  Ты получил:\n\n"
    )

    # Формируем строки по одной карте с эмодзи
    card_lines = []
    for c in cards:
        card_lines.append(f"    {format_card_short(c)}")

    # Отправляем все сразу, но с разделителями
    body = "\n".join(card_lines)
    footer = (
        f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 Потрачено: {result['price']}\n"
        f"💵 Осталось: {u.coins - result['price']}"
    )

    await msg.edit_text(intro + body + footer, reply_markup=after_pack_keyboard())
    await callback.answer(f"{emoji} Пак открыт!")


def register_handlers(dp):
    dp.callback_query.register(buy_pack, F.data.startswith("pack_"))
