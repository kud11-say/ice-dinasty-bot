from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль", callback_data="menu_profile"),
         InlineKeyboardButton(text="🃏 Коллекция", callback_data="menu_collection")],
        [InlineKeyboardButton(text="🏒 Состав", callback_data="menu_team"),
         InlineKeyboardButton(text="⚔️ Матчи", callback_data="menu_matches")],
        [InlineKeyboardButton(text="🏆 Сезон", callback_data="menu_season"),
         InlineKeyboardButton(text="🛒 Магазин", callback_data="menu_shop")],
        [InlineKeyboardButton(text="📦 Открыть пак", callback_data="menu_packs"),
         InlineKeyboardButton(text="⚙️ Настройки", callback_data="menu_settings")],
    ])
