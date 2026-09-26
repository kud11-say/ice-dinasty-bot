from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def age_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="18–25 лет", callback_data="age_21")],
        [InlineKeyboardButton(text="26–40 лет", callback_data="age_33")],
        [InlineKeyboardButton(text="41–55 лет", callback_data="age_48")],
        [InlineKeyboardButton(text="56–70 лет", callback_data="age_63")],
    ])


def origin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏒 Бывший игрок", callback_data="origin_player")],
        [InlineKeyboardButton(text="📊 Аналитик", callback_data="origin_analyst")],
        [InlineKeyboardButton(text="💼 Бизнесмен", callback_data="origin_business")],
        [InlineKeyboardButton(text="🎓 Выпускник", callback_data="origin_graduate")],
        [InlineKeyboardButton(text="🎙 Журналист", callback_data="origin_journalist")],
        [InlineKeyboardButton(text="🌍 Иностранец", callback_data="origin_foreigner")],
    ])


def club_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏒 ТОРОС (Нефтекамск)", callback_data="club_toros")],
        [InlineKeyboardButton(text="🏒 БУРАН (Воронеж)", callback_data="club_buran")],
        [InlineKeyboardButton(text="🏒 АКМ (Тульская обл.)", callback_data="club_akm")],
    ])


def def confirm_club_keyboard(club_key: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, играю", callback_data=f"confirm_club_{club_key}")],
        [InlineKeyboardButton(text="⬅️ Выбрать другой", callback_data="back_to_clubs")],
    ])

def skip_slogan_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭ Пропустить", callback_data="skip_slogan")],
    ])


def confirm_registration_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Погнали!", callback_data="finish_registration")],
        [InlineKeyboardButton(text="🔄 Начать заново", callback_data="restart_registration")],
    ])
