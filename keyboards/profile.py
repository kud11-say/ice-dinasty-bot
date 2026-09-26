from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Достижения", callback_data="profile_achiev")],
        [InlineKeyboardButton(text="📜 Журнал", callback_data="profile_journal")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])
