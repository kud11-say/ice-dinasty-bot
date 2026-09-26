import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN, ADMIN_ID
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    text = (
        "🏒 ICE DYNASTY\n"
        "─────────────────────\n\n"
        f"Привет, {user.first_name}!\n\n"
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
async def start_career(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🚧 РАЗДЕЛ В РАЗРАБОТКЕ\n"
        "─────────────────────\n\n"
        "Регистрация и онбординг появятся "
        "в ближайшем обновлении."
    )
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
    
    # Инициализация базы данных
    logger.info("🗄️ Инициализация базы данных...")
    await init_db()
    logger.info("✅ База данных готова.")
    
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Бот запущен. Ожидаю сообщения...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
