from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def team_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Автосостав", callback_data="team_auto")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])
