from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


RARITY_EMOJI = {
    "bronze": "🥉",
    "silver": "🥈",
    "gold": "🥇",
    "elite": "💎",
    "legend": "👑",
    "icon": "🌟",
}


def collection_keyboard(cards: list):
    """Клавиатура коллекции — кнопки с карточками."""
    buttons = []
    row = []
    
    for i, item in enumerate(cards):
        card = item["card"]
        user_card = item["user_card"]
        rarity = RARITY_EMOJI.get(card.rarity, "❓")
        text = f"{rarity} {card.name} ({card.ovr})"
        row.append(InlineKeyboardButton(text=text, callback_data=f"card_view_{user_card.id}"))
        
        if len(row) == 2:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def card_detail_keyboard(user_card_id: int):
    """Клавиатура деталей карточки."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Тренировать", callback_data=f"card_train_{user_card_id}")],
        [InlineKeyboardButton(text="⬅️ К коллекции", callback_data="back_to_collection")],
    ])
