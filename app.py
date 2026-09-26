import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_ID
from database import init_db

from handlers import registration, menu

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def cmd_start(message: Message, state):
    from database import async_session
    from models import User
    from sqlalchemy import select
    
    user_id = message.from_user.id
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
    
    if user and user.is_registered:
        text = (
            "🏒 ICE DYNASTY\n"
            "─────────────────────\n\n"
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
        "🏒 ICE DYNASTY\n"
        "─────────────────────\n\n"
        f"Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в игру, где ты станешь "
        "генеральным менеджером хоккейного клуба.\n\n"
        "Собирай команду, играй матчи, "
        "проходи сюжет и строй династию.\n\n"
        "Готов начать карьеру?"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Начать", callback_data="start_career")],
        [InlineKeyboardButton(text="📖 Что это за игра?", callback_data="about_game")],
    ])
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "about_game")
async def about_game(callback: types.CallbackQuery):
    text = (
        "📖 ЧТО ТАКОЕ ICE DYNASTY?\n"
        "─────────────────────\n\n"
        "Это текстовая игра про хоккей.\n"
        "Ты — генеральный менеджер клуба.\n\n"
        "Твоя задача:\n"
        "• Найти игроков\n"
        "• Собрать состав\n"
        "• Выиграть Кубок\n\n"
        "Игра идёт по сезонам.\n"
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
        "🏒 ICE DYNASTY\n"
        "─────────────────────\n\n"
        "Готов начать карьеру?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎬 Начать", callback_data="start_career")],
            [InlineKeyboardButton(text="📖 Что это за игра?", callback_data="about_game")],
        ])
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "start_career")
async def start_career(callback: types.CallbackQuery, state):
    await registration.start_registration(callback.from_user.id, callback.message, state)
    await callback.answer()


@dp.callback_query(lambda c: c.data == "continue_game")
async def continue_game(callback: types.CallbackQuery):
    await menu.render_menu(callback.from_user.id, callback.message, edit=True)
    await callback.answer()


@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа.")
        return
    await message.answer(
        "🛡️ GOD MODE\n"
        "─────────────────────\n\n"
        "✅ Бот работает.\n"
        "✅ Переменные загружены.\n"
        "✅ Админ-доступ подтверждён.\n"
        "✅ База данных подключена.\n\n"
        f"Ваш ID: {message.from_user.id}"
    )


async def main():
    logger.info("🏒 Ice Dynasty Bot запускается...")
    logger.info(f"Админ ID: {ADMIN_ID}")
    
    logger.info("🗄️ Инициализация базы данных...")
    await init_db()
    logger.info("✅ База данных готова.")
    
    # Генерация карточек (если база пуста)
    try:
        from services.card_generator import generate_cards_if_empty
        logger.info("🃏 Проверка базы карточек...")
        await generate_cards_if_empty()
        logger.info("✅ База карточек готова.")
    except Exception as e:
        logger.error(f"⚠️ Ошибка генерации карточек: {e}")
    
    from handlers import registration, menu, collection
registration.register_handlers(dp)
menu.register_handlers(dp)
collection.register_handlers(dp)
await bot.delete_webhook(drop_pending_updates=True)
logger.info("✅ Бот запущен. Ожидаю сообщения...")
await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
