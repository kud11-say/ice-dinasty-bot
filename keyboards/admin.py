from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_main_keyboard():
    """Главное меню God Mode — 15 разделов."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Игроки", callback_data="adm_players"),
         InlineKeyboardButton(text="💰 Экономика", callback_data="adm_economy")],

        [InlineKeyboardButton(text="🎁 Выдать", callback_data="adm_give"),
         InlineKeyboardButton(text="⚡ Энергия", callback_data="adm_energy")],

        [InlineKeyboardButton(text="🃏 Карточки", callback_data="adm_cards"),
         InlineKeyboardButton(text="📖 Сюжет", callback_data="adm_story")],

        [InlineKeyboardButton(text="📊 Статистика", callback_data="adm_stats"),
         InlineKeyboardButton(text="📨 Рассылка", callback_data="adm_broadcast")],

        [InlineKeyboardButton(text="🚫 Модерация", callback_data="adm_moderation"),
         InlineKeyboardButton(text="💾 Бэкап", callback_data="adm_backup")],

        [InlineKeyboardButton(text="⚙️ Система", callback_data="adm_system"),
         InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])


def admin_players_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Найти по @username", callback_data="adm_find_user")],
        [InlineKeyboardButton(text="🎁 Выдать стартовый пак себе", callback_data="adm_self_pack")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="adm_back")],
    ])


def admin_economy_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 +10 000 монет", callback_data="adm_coins_10k")],
        [InlineKeyboardButton(text="💰 +100 000 монет", callback_data="adm_coins_100k")],
        [InlineKeyboardButton(text="💎 +100 рубинов", callback_data="adm_rubies_100")],
        [InlineKeyboardButton(text="💎 +1000 рубинов", callback_data="adm_rubies_1000")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="adm_back")],
    ])


def admin_cards_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Стартовый пак себе", callback_data="adm_self_pack")],
        [InlineKeyboardButton(text="🃏 Выдать легенду", callback_data="adm_give_legend")],
        [InlineKeyboardButton(text="🏒 Выдать 5 золотых", callback_data="adm_give_gold")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="adm_back")],
    ])


def admin_story_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Глава 1: Пролог", callback_data="adm_story_ch1")],
        [InlineKeyboardButton(text="📖 Глава 2 (разблокировать)", callback_data="adm_story_ch2")],
        [InlineKeyboardButton(text="🔄 Сбросить сюжет", callback_data="adm_story_reset")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="adm_back")],
    ])


def admin_moderation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Забанить @username", callback_data="adm_ban_user")],
        [InlineKeyboardButton(text="✅ Разбанить @username", callback_data="adm_unban_user")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="adm_back")],
    ])


def admin_system_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Рестарт бота", callback_data="adm_restart")],
        [InlineKeyboardButton(text="📊 Проверка БД", callback_data="adm_db_check")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="adm_back")],
    ])


def admin_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В God Mode", callback_data="adm_back")],
    ])
