from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_ID
from database import async_session
from models import User, Card
from sqlalchemy import select, func


def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Выдать стартовый пак", callback_data="admin_give_pack")],
        [InlineKeyboardButton(text="💰 +10 000 монет", callback_data="admin_coins")],
        [InlineKeyboardButton(text="💎 +100 рубинов", callback_data="admin_rubies")],
        [InlineKeyboardButton(text="⚡ Восстановить энергию", callback_data="admin_energy")],
        [InlineKeyboardButton(text="📊 Статистика базы", callback_data="admin_stats")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])


async def cmd_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа.")
        return
    await message.answer(
        "🛡️ GOD MODE\n─────────────────────\n\n"
        "Выбери действие:",
        reply_markup=admin_keyboard()
    )


async def admin_give_pack(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔", show_alert=True)
        return
    from services.card_service import give_starter_pack, format_card_short
    cards = await give_starter_pack(callback.from_user.id)
    cards_text = "\n".join([format_card_short(c) for c in cards]) if cards else "—"
    await callback.message.edit_text(
        "🎁 СТАРТОВЫЙ ПАК ВЫДАН\n─────────────────────\n"
        f"{cards_text}",
        reply_markup=admin_keyboard()
    )
    await callback.answer("Готово!")


async def admin_coins(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔", show_alert=True)
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.coins += 10000
            await session.commit()
    await callback.answer("💰 +10 000 монет!")


async def admin_rubies(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔", show_alert=True)
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.rubies += 100
            await session.commit()
    await callback.answer("💎 +100 рубинов!")


async def admin_energy(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔", show_alert=True)
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.energy = 20
            await session.commit()
    await callback.answer("⚡ Энергия восстановлена!")


async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔", show_alert=True)
        return
    async with async_session() as session:
        users_count = await session.scalar(select(func.count(User.id)))
        cards_count = await session.scalar(select(func.count(Card.id)))
    await callback.message.edit_text(
        "📊 СТАТИСТИКА БАЗЫ\n─────────────────────\n"
        f"👥 Игроков: {users_count or 0}\n"
        f"🃏 Карточек: {cards_count or 0}",
        reply_markup=admin_keyboard()
    )
    await callback.answer()


def register_handlers(dp):
    dp.message.register(cmd_admin, Command("admin"))
    dp.callback_query.register(admin_give_pack, F.data == "admin_give_pack")
    dp.callback_query.register(admin_coins, F.data == "admin_coins")
    dp.callback_query.register(admin_rubies, F.data == "admin_rubies")
    dp.callback_query.register(admin_energy, F.data == "admin_energy")
    dp.callback_query.register(admin_stats, F.data == "admin_stats")
