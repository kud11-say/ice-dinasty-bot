from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def season_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Таблица лиги", callback_data="season_table")],
        [InlineKeyboardButton(text="🏆 Плей-офф", callback_data="season_playoff")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])
