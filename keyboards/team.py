from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def team_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Автосостав", callback_data="team_auto")],
        [InlineKeyboardButton(text="👑 Капитан и ассистенты", callback_data="team_roles")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])


def team_empty_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🃏 В коллекцию", callback_data="menu_collection")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])
