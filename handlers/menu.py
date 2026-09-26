from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import async_session
from models import User
from sqlalchemy import select

from keyboards.main_menu import main_menu_keyboard


async def cmd_menu(message: Message):
    user_id = message.from_user.id
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
    
    if not user or not user.is_registered:
        await message.answer("Сначала зарегистрируйся: /start")
        return
    
    text = (
        "🏒 ICE DYNASTY\n"
        "─────────────────────\n"
        f"{user.name} | ГМ «{user.club}»\n"
        f"Ур. {user.level} • 💰 {user.coins} • 💎 {user.rubies}\n"
        f"⚡ {user.energy} / 20\n"
        "─────────────────────\n"
        "Выбери раздел:"
    )
    
    await message.answer(text, reply_markup=main_menu_keyboard())


async def menu_profile(callback: CallbackQuery):
    await callback.answer("👤 Профиль — скоро!", show_alert=True)


async def menu_collection(callback: CallbackQuery):
    await callback.answer("🃏 Коллекция — скоро!", show_alert=True)


async def menu_team(callback: CallbackQuery):
    await callback.answer("🏒 Состав — скоро!", show_alert=True)


async def menu_matches(callback: CallbackQuery):
    await callback.answer("⚔️ Матчи — скоро!", show_alert=True)


async def menu_season(callback: CallbackQuery):
    await callback.answer("🏆 Сезон — скоро!", show_alert=True)


async def menu_shop(callback: CallbackQuery):
    await callback.answer("🛒 Магазин — скоро!", show_alert=True)


async def menu_social(callback: CallbackQuery):
    await callback.answer("👥 Социальное — скоро!", show_alert=True)


async def menu_settings(callback: CallbackQuery):
    await callback.answer("⚙️ Настройки — скоро!", show_alert=True)


def register_handlers(dp):
    dp.message.register(cmd_menu, Command("menu"))
    dp.callback_query.register(menu_profile, F.data == "menu_profile")
    dp.callback_query.register(menu_collection, F.data == "menu_collection")
    dp.callback_query.register(menu_team, F.data == "menu_team")
    dp.callback_query.register(menu_matches, F.data == "menu_matches")
    dp.callback_query.register(menu_season, F.data == "menu_season")
    dp.callback_query.register(menu_shop, F.data == "menu_shop")
    dp.callback_query.register(menu_social, F.data == "menu_social")
    dp.callback_query.register(menu_settings, F.data == "menu_settings")
