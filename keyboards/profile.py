from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])
