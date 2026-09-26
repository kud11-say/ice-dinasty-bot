from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Выдать стартовый пак", callback_data="admin_give_pack")],
        [InlineKeyboardButton(text="💰 +10 000 монет", callback_data="admin_coins")],
        [InlineKeyboardButton(text="💎 +100 рубинов", callback_data="admin_rubies")],
        [InlineKeyboardButton(text="⚡ Восстановить энергию", callback_data="admin_energy")],
        [InlineKeyboardButton(text="📊 Статистика базы", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📖 Дойти до сюжета", callback_data="admin_story")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])
