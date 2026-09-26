from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


RARITY_EMOJI = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "elite": "💎", "legend": "👑", "icon": "🌟"}


def collection_keyboard(cards: list):
    buttons = []
    row = []
    for item in cards:
        card = item["card"]
        user_card = item["user_card"]
        rarity = RARITY_EMOJI.get(card.rarity, "❓")
        text = f"{rarity} {card.name[:14]} ({card.ovr})"
        row.append(InlineKeyboardButton(text=text, callback_data=f"card_view_{user_card.id}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def card_detail_keyboard(user_card_id: int, in_team: bool = False):
    rows = []
    if not in_team:
        rows.append([InlineKeyboardButton(text="➕ В состав", callback_data=f"card_to_team_{user_card_id}")])
    else:
        rows.append([InlineKeyboardButton(text="➖ Из состава", callback_data=f"card_from_team_{user_card_id}")])
    rows.append([InlineKeyboardButton(text="⬅️ К коллекции", callback_data="back_to_collection")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
