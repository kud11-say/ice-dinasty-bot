import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, ADMIN_ID
from database import init_db

from handlers import (
    registration, menu, collection, profile, team,
    packs, matches, season, admin, story
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher(storage=MemoryStorage())


# ─── /start ─────────────────────────────────────

@dp.message(CommandStart())
async def cmd_start(message: Message, state):
    try:
        await state.clear()
    except Exception:
        pass

    logger.info(f"📥 /start от {message.from_user.id}")

    try:
        from database import async_session
        from models import User
        from sqlalchemy import select

        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == message.from_user.id))
            user = result.scalar_one_or_none()

        if user and user.is_registered:
            text = (
                "🏒  ICE DYNASTY\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"С возвращением, {user.name}!\n\n"
                "Продолжим?"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="▶️ Продолжить", callback_data="continue_game")],
                [InlineKeyboardButton(text="👤 Профиль", callback_data="menu_profile")],
            ])
            await message.answer(text, reply_markup=keyboard)
            return

        text = (
            "🏒  ICE DYNASTY\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Привет, {message.from_user.first_name}!\n\n"
            "Добро пожаловать в игру, где ты станешь "
            "генеральным менеджером хоккейного клуба.\n\n"
            "Собирай команду, играй матчи, "
            "проходи сюжет и строй династию.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Готов начать карьеру?"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎬 Начать", callback_data="start_career")],
            [InlineKeyboardButton(text="📖 Что это за игра?", callback_data="about_game")],
        ])
        await message.answer(text, reply_markup=keyboard)
    except Exception as e:
        logger.exception(f"❌ Ошибка в /start: {e}")
        await message.answer(f"❌ Ошибка: {e}")


# ─── /menu ──────────────────────────────────────

@dp.message(Command("menu"))
async def cmd_menu_direct(message: Message, state):
    try:
        await state.clear()
    except Exception:
        pass

    logger.info(f"📥 /menu от {message.from_user.id}")

    try:
        await menu.render_menu(message.from_user.id, message)
    except Exception as e:
        logger.exception(f"❌ Ошибка в /menu: {e}")
        await message.answer(f"❌ Ошибка: {e}")


# ─── ХЕЛП ───────────────────────────────────────

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🏒  ICE DYNASTY — ПОМОЩЬ\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "/start — начать / продолжить\n"
        "/menu — главное меню\n"
        "/admin — God Mode\n"
        "/help — эта справка\n"
    )


# ─── CALLBACK: ПРОДОЛЖИТЬ ──────────────────────

@dp.callback_query(lambda c: c.data == "continue_game")
async def continue_game(callback: types.CallbackQuery):
    await menu.render_menu(callback.from_user.id, callback.message, edit=True)
    await callback.answer()


@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await menu.render_menu(callback.from_user.id, callback.message, edit=True)
    await callback.answer()


# ─── CALLBACK: О ИГРЕ ──────────────────────────

@dp.callback_query(lambda c: c.data == "about_game")
async def about_game(callback: types.CallbackQuery):
    text = (
        "📖  ЧТО ТАКОЕ ICE DYNASTY?\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Это текстовая игра про хоккей.\n"
        "Ты — генеральный менеджер клуба.\n\n"
        "Твоя задача:\n"
        "• Найти игроков\n"
        "• Собрать состав\n"
        "• Выиграть Кубок\n\n"
        "Игра идёт по сезонам.\n"
        "Один сезон = одна глава сюжета.\n\n"
        "Это бесплатно. Это навсегда."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Начать", callback_data="start_career")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")],
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🏒  ICE DYNASTY\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Готов начать карьеру?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎬 Начать", callback_data="start_career")],
            [InlineKeyboardButton(text="📖 Что это за игра?", callback_data="about_game")],
        ])
    )
    await callback.answer()


# ─── CALLBACK: СТАРТ КАРЬЕРЫ ───────────────────

@dp.callback_query(lambda c: c.data == "start_career")
async def start_career(callback: types.CallbackQuery, state):
    await state.clear()
    await registration.start_registration(callback.from_user.id, callback.message, state)
    await callback.answer()


# ─── CALLBACK: КНОПКИ МЕНЮ ─────────────────────

@dp.callback_query(lambda c: c.data == "menu_profile")
async def btn_profile(callback: types.CallbackQuery):
    try:
        await menu.menu_profile(callback)
    except Exception as e:
        logger.exception(f"Ошибка profile: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_collection")
async def btn_collection(callback: types.CallbackQuery):
    try:
        await menu.menu_collection(callback)
    except Exception as e:
        logger.exception(f"Ошибка collection: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_team")
async def btn_team(callback: types.CallbackQuery):
    try:
        await menu.menu_team(callback)
    except Exception as e:
        logger.exception(f"Ошибка team: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_matches")
async def btn_matches(callback: types.CallbackQuery):
    try:
        from handlers.matches import show_matches
        await show_matches(callback)
    except Exception as e:
        logger.exception(f"Ошибка matches: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_season")
async def btn_season(callback: types.CallbackQuery):
    try:
        await menu.menu_season(callback)
    except Exception as e:
        logger.exception(f"Ошибка season: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_shop")
async def btn_shop(callback: types.CallbackQuery):
    try:
        await menu.menu_shop(callback)
    except Exception as e:
        logger.exception(f"Ошибка shop: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_story")
async def btn_story(callback: types.CallbackQuery):
    try:
        from handlers.story import show_story
        await show_story(callback)
    except Exception as e:
        logger.exception(f"Ошибка story: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)


@dp.callback_query(lambda c: c.data == "menu_settings")
async def btn_settings(callback: types.CallbackQuery):
    await callback.answer("⚙️ Скоро!", show_alert=True)


# ─── ФОНОВАЯ ГЕНЕРАЦИЯ ─────────────────────────

async def generate_cards_background():
    try:
        from services.card_generator import generate_cards_if_empty
        count = await generate_cards_if_empty()
        if count:
            logger.info(f"✅ Сгенерировано карточек: {count}")
        else:
            logger.info("✅ Карточки уже в базе")
    except Exception as e:
        logger.error(f"⚠️ Ошибка генерации: {e}")


# ─── MAIN ──────────────────────────────────────

async def main():
    logger.info("🏒 Ice Dynasty Bot запускается...")
    await init_db()
    logger.info("✅ База данных готова.")

    registration.register_handlers(dp)
    collection.register_handlers(dp)
    team.register_handlers(dp)
    packs.register_handlers(dp)
    matches.register_handlers(dp)
    admin.register_handlers(dp)
    story.register_handlers(dp)
    profile.register_handlers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(generate_cards_background())

    logger.info("✅ Бот запущен. Ожидаю сообщения...")
    await dp.start_polling(bot, polling_timeout=60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
