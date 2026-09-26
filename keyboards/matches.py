from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def match_tactic_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Атакующая", callback_data="match_tactic_attack")],
        [InlineKeyboardButton(text="🛡 Оборонительная", callback_data="match_tactic_defense")],
        [InlineKeyboardButton(text="💪 Прессинг", callback_data="match_tactic_press")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])


def after_match_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Ещё матч", callback_data="menu_matches")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])
