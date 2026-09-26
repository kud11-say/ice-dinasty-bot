from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def packs_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥉 Бронзовый — 1 000", callback_data="pack_bronze")],
        [InlineKeyboardButton(text="🥈 Серебряный — 5 000", callback_data="pack_silver")],
        [InlineKeyboardButton(text="🥇 Золотой — 15 000", callback_data="pack_gold")],
        [InlineKeyboardButton(text="💎 Элитный — 50 000", callback_data="pack_elite")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ])


def after_pack_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Ещё пак", callback_data="menu_shop")],
        [InlineKeyboardButton(text="🃏 В коллекцию", callback_data="menu_collection")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])
