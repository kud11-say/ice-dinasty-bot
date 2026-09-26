from aiogram.types import Message, CallbackQuery
import logging

from database import async_session
from models import User
from sqlalchemy import select
from keyboards.main_menu import main_menu_keyboard
from data.clubs import club_emoji

logger = logging.getLogger(__name__)


async def render_menu(user_id: int, target, edit: bool = False):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

    if not user or not user.is_registered:
        text = "Сначала зарегистрируйся: /start"
        if edit:
            await target.edit_text(text)
        else:
            await target.answer(text)
        return

    club_em = club_emoji(user.club)
    text = (
        "🏒  ICE DYNASTY\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{club_em}  {user.name}  |  ГМ «{user.club}»\n"
        f"Ур. {user.level}  •  💰 {user.coins}  •  💎 {user.rubies}\n"
        f"⚡ {user.energy}/20\n"
        f"📖 Глава {user.chapter}  •  День {user.day}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Выбери раздел:"
    )

    if edit:
        await target.edit_text(text, reply_markup=main_menu_keyboard())
    else:
        await target.answer(text, reply_markup=main_menu_keyboard())


async def cmd_menu(message: Message):
    await render_menu(message.from_user.id, message)


async def menu_profile(callback: CallbackQuery):
    from handlers.profile import show_profile
    await show_profile(callback)


async def menu_collection(callback: CallbackQuery):
    from handlers.collection import show_collection
    await show_collection(callback)


async def menu_team(callback: CallbackQuery):
    from handlers.team import show_team
    await show_team(callback)


async def menu_matches(callback: CallbackQuery):
    from handlers.matches import show_matches
    await show_matches(callback)


async def menu_season(callback: CallbackQuery):
    from handlers.season import show_season
    await show_season(callback)


async def menu_shop(callback: CallbackQuery):
    from handlers.packs import show_packs
    await show_packs(callback)


async def menu_packs(callback: CallbackQuery):
    from handlers.packs import show_packs
    await show_packs(callback)


async def menu_settings(callback: CallbackQuery):
    await callback.answer("⚙️ Скоро!", show_alert=True)
