from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def story_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Начать главу", callback_data="story_start_ch1")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])


def story_choice_keyboard(choices: list):
    rows = [[InlineKeyboardButton(text=t, callback_data=cb)] for t, cb in choices]
    rows.append([InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def story_next_keyboard(next_data: str, next_text: str = "▶️ Дальше"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=next_text, callback_data=next_data)],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_to_menu")],
    ])
