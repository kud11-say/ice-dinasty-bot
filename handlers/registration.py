from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from database import async_session
from models import User
from sqlalchemy import select

from keyboards.registration import (
    age_keyboard, origin_keyboard, club_keyboard,
    confirm_club_keyboard, skip_slogan_keyboard,
    confirm_registration_keyboard
)


class Registration(StatesGroup):
    name = State()
    age = State()
    origin = State()
    club = State()
    slogan = State()


TEMP_DATA = {}
ORIGINS = {"player": "🏒 Бывший игрок", "analyst": "📊 Аналитик", "business": "💼 Бизнесмен",
           "graduate": "🎓 Выпускник", "journalist": "🎙 Журналист", "foreigner": "🌍 Иностранец"}
CLUBS = {
    "toros": {"name": "Торос", "city": "Нефтекамск", "league": "VHL"},
    "buran": {"name": "Буран", "city": "Воронеж", "league": "VHL"},
    "akm": {"name": "АКМ", "city": "Тульская обл.", "league": "VHL"},
}


def get_data(user_id: int) -> dict:
    if user_id not in TEMP_DATA:
        TEMP_DATA[user_id] = {}
    return TEMP_DATA[user_id]


async def start_registration(user_id: int, message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user and user.is_registered:
            await message.answer("Ты уже зарегистрирован! Используй /menu.")
            return

    TEMP_DATA[user_id] = {}
    await state.set_state(Registration.name)
    await message.answer(
        "📝 РЕГИСТРАЦИЯ • 1/5\n"
        "─────────────────────\n\n"
        "Как тебя зовут?\n\n"
        "Это имя увидят болельщики, пресса "
        "и твои игроки. Выбери с умом — "
        "изменить можно раз в сезон.\n\n"
        "✏️ Напиши имя (3–20 символов):"
    )


async def process_name(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else ""
    if len(name) < 3 or len(name) > 20:
        await message.answer("⚠️ Имя должно быть от 3 до 20 символов.")
        return
    if not all(c.isalnum() or c in " -_" for c in name):
        await message.answer("⚠️ Только буквы, цифры, пробел, дефис и подчёркивание.")
        return
    user_id = message.from_user.id
    get_data(user_id)["name"] = name
    await state.set_state(Registration.age)
    await message.answer(
        "📝 РЕГИСТРАЦИЯ • 2/5\n─────────────────────\n\n"
        f"Отлично, {name}!\n\nСколько тебе лет?",
        reply_markup=age_keyboard()
    )


async def process_age(callback: CallbackQuery, state: FSMContext):
    age = int(callback.data.split("_")[1])
    get_data(callback.from_user.id)["age"] = age
    await state.set_state(Registration.origin)
    await callback.message.edit_text(
        "📝 РЕГИСТРАЦИЯ • 3/5\n─────────────────────\n\n"
        "Кем ты был до карьеры ГМ?",
        reply_markup=origin_keyboard()
    )
    await callback.answer()


async def process_origin(callback: CallbackQuery, state: FSMContext):
    origin = callback.data.replace("origin_", "")
    get_data(callback.from_user.id)["origin"] = origin
    await state.set_state(Registration.club)
    await callback.message.edit_text(
        "📝 РЕГИСТРАЦИЯ • 4/5\n─────────────────────\n\n"
        "Выбери свой клуб:\n\n"
        "🏒 ТОРОС — династия. ⭐⭐\n"
        "🏒 БУРАН — выживание. ⭐⭐⭐\n"
        "🏒 АКМ — новая кровь. ⭐",
        reply_markup=club_keyboard()
    )
    await callback.answer()


async def process_club(callback: CallbackQuery, state: FSMContext):
    club_key = callback.data.replace("club_", "")
    club = CLUBS[club_key]
    get_data(callback.from_user.id)["club"] = club_key
    await callback.message.edit_text(
        f"✅ Ты выбрал «{club['name']}»\n─────────────────────\n\n"
        "Ты уверен? Изменить клуб можно только через новый аккаунт.",
        reply_markup=confirm_club_keyboard(club_key)
    )
    await callback.answer()


async def back_to_clubs(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 РЕГИСТРАЦИЯ • 4/5\n─────────────────────\n\nВыбери свой клуб:",
        reply_markup=club_keyboard()
    )
    await callback.answer()


async def confirm_club(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.slogan)
    await callback.message.edit_text(
        "📝 РЕГИСТРАЦИЯ • 5/5\n─────────────────────\n\n"
        "Придумай слоган клуба (до 30 символов) или пропусти:",
        reply_markup=skip_slogan_keyboard()
    )
    await callback.answer()


async def process_slogan(message: Message, state: FSMContext):
    slogan = message.text.strip()[:30] if message.text else "Мы — одна команда"
    get_data(message.from_user.id)["slogan"] = slogan
    await show_confirmation(message, message.from_user.id, edit=False)


async def skip_slogan(callback: CallbackQuery, state: FSMContext):
    get_data(callback.from_user.id)["slogan"] = "Мы — одна команда"
    await show_confirmation(callback.message, callback.from_user.id, edit=True)
    await callback.answer()


async def show_confirmation(message, user_id: int, edit: bool = False):
    data = get_data(user_id)
    if "name" not in data or "club" not in data:
        await message.answer("⚠️ Что-то пошло не так. /start")
        return
    club = CLUBS[data["club"]]
    text = (
        "🎉 РЕГИСТРАЦИЯ ЗАВЕРШЕНА\n─────────────────────\n\n"
        f"Имя: {data['name']}\nВозраст: {data.get('age', 25)}\n"
        f"Происхождение: {ORIGINS.get(data.get('origin', 'player'))}\n"
        f"Клуб: {club['name']}\nСлоган: «{data['slogan']}»\n\n"
        "Стартовые бонусы:\n💰 5000 монет\n💎 10 рубинов\n⚡ 20/20\n🃏 Стартовый пак (5 карточек)\n\n"
        "Готов начать?"
    )
    if edit:
        await message.edit_text(text, reply_markup=confirm_registration_keyboard())
    else:
        await message.answer(text, reply_markup=confirm_registration_keyboard())


async def finish_registration(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = TEMP_DATA.get(user_id)
    if not data or "name" not in data or "club" not in data:
        await callback.message.edit_text("⚠️ Что-то пошло не так. /start")
        return
    club = CLUBS[data["club"]]

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(id=user_id)
            session.add(user)
        user.username = callback.from_user.username
        user.name = data["name"]
        user.age = data.get("age", 25)
        user.origin = data.get("origin", "player")
        user.club = club["name"]
        user.league = club["league"]
        user.is_registered = True
        await session.commit()

    from services.card_service import give_starter_pack, format_card_short
    starter_cards = await give_starter_pack(user_id)
    cards_text = "\n".join([format_card_short(c) for c in starter_cards]) if starter_cards else "—"

    await state.clear()
    TEMP_DATA.pop(user_id, None)

    await callback.message.edit_text(
        "🎬 КАБИНЕТ ДИРЕКТОРА\n─────────────────────\n\n"
        "Виктор Петрович смотрит на тебя поверх очков.\n\n"
        "«Итак. Ты — новый ГМ. Клуб в кризисе.\n"
        "Задача: выйти в плей-офф. Держи стартовый набор.»\n\n"
        "─────────────────────\n"
        "🎁 СТАРТОВЫЙ ПАК:\n"
        f"{cards_text}\n\n"
        "─────────────────────\n"
        "Напиши /menu для продолжения."
    )
    await callback.answer("Добро пожаловать в Ice Dynasty!")


def register_handlers(dp):
    dp.callback_query.register(process_age, F.data.startswith("age_"))
    dp.callback_query.register(process_origin, F.data.startswith("origin_"))
    dp.callback_query.register(process_club, F.data.startswith("club_"))
    dp.callback_query.register(back_to_clubs, F.data == "back_to_clubs")
    dp.callback_query.register(confirm_club, F.data.startswith("confirm_club_"))
    dp.callback_query.register(skip_slogan, F.data == "skip_slogan")
    dp.callback_query.register(finish_registration, F.data == "finish_registration")
    dp.message.register(process_name, Registration.name)
    dp.message.register(process_slogan, Registration.slogan)
