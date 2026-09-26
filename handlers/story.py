from aiogram import F
from aiogram.types import CallbackQuery

from database import async_session
from models import User
from sqlalchemy import select
from keyboards.story import story_start_keyboard, story_choice_keyboard, story_next_keyboard


async def show_story(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()

    if not user:
        await callback.answer("Ошибка", show_alert=True)
        return

    text = (
        "📖 СЮЖЕТ\n"
        "─────────────────────\n\n"
        f"Текущая глава: {user.chapter}\n"
        f"День сезона: {user.day}\n\n"
        "Глава 1: «Провинциалы»\n"
        "Ты — молодой ГМ. Клуб в кризисе.\n\n"
        "Начать главу?"
    )
    await callback.message.edit_text(text, reply_markup=story_start_keyboard())
    await callback.answer()


async def start_ch1(callback: CallbackQuery):
    text = (
        "📖 ГЛАВА 1: «ПРОВИНЦИАЛЫ»\n"
        "─────────────────────\n\n"
        "Кабинет директора. Пахнет старым деревом "
        "и табаком.\n\n"
        "Виктор Петрович Соколов сидит за столом. "
        "Перед ним — кипа бумаг и старый телефон.\n\n"
        "«Итак. Ты — новый ГМ. Клуб в кризисе. "
        "Денег нет. Состав — вот он.\n\n"
        "Задача: выйти в плей-офф. Или я найду "
        "другого ГМ.»\n\n"
        "Он смотрит на тебя, ожидая ответа."
    )
    choices = [
        ("«Я справлюсь.»", "story_ch1_answer_yes"),
        ("«Расскажите подробнее.»", "story_ch1_answer_ask"),
        ("«Почему я?»", "story_ch1_answer_why"),
    ]
    await callback.message.edit_text(text, reply_markup=story_choice_keyboard(choices))
    await callback.answer()


async def answer_yes(callback: CallbackQuery):
    text = (
        "📖 КАБИНЕТ ДИРЕКТОРА\n"
        "─────────────────────\n\n"
        "Соколов усмехается.\n\n"
        "«Уверенность — это хорошо. Но уверенность "
        "без результата — это самоуверенность.\n\n"
        "Держи стартовый набор. Собери что-нибудь "
        "из этого.»\n\n"
        "Он кидает тебе на стол конверт.\n\n"
        "─────────────────────\n"
        "📌 ЗАДАЧА: выйти в плей-офф ВХЛ."
    )
    await callback.message.edit_text(text, reply_markup=story_next_keyboard("story_ch1_done"))
    await callback.answer()


async def answer_ask(callback: CallbackQuery):
    text = (
        "📖 КАБИНЕТ ДИРЕКТОРА\n"
        "─────────────────────\n\n"
        "Соколов хмурится.\n\n"
        "«Подробнее? Клуб в долгах. Состав старый. "
        "Болельщики не ходят. Тренер на грани "
        "увольнения.\n\n"
        "Достаточно подробно?»\n\n"
        "Он замолкает, давая тебе время "
        "осознать."
    )
    await callback.message.edit_text(text, reply_markup=story_next_keyboard("story_ch1_after_ask"))
    await callback.answer()


async def answer_why(callback: CallbackQuery):
    text = (
        "📖 КАБИНЕТ ДИРЕКТОРА\n"
        "─────────────────────\n\n"
        "Соколов долго смотрит на тебя.\n\n"
        "«Потому что никто другой не согласился.\n\n"
        "Клуб умирает. Тебе дали шанс. "
        "Или ты вытащишь его, или пойдёшь на дно "
        "вместе с ним.\n\n"
        "Выбирай.»"
    )
    await callback.message.edit_text(text, reply_markup=story_next_keyboard("story_ch1_after_why"))
    await callback.answer()


async def after_ask(callback: CallbackQuery):
    text = (
        "📖 КАБИНЕТ ДИРЕКТОРА\n"
        "─────────────────────\n\n"
        "«Хватит вопросов. Вот стартовый набор. "
        "Собери команду. Первый матч — через "
        "неделю.»\n\n"
        "Он встаёт, давая понять, что разговор "
        "закончен."
    )
    await callback.message.edit_text(text, reply_markup=story_next_keyboard("story_ch1_done"))
    await callback.answer()


async def after_why(callback: CallbackQuery):
    text = (
        "📖 КАБИНЕТ ДИРЕКТОРА\n"
        "─────────────────────\n\n"
        "Соколов кивает, будто услышал "
        "правильный ответ.\n\n"
        "«Вот это уже похоже на ГМ. Держи набор. "
        "Работай.»\n\n"
        "Он бросает конверт через стол."
    )
    await callback.message.edit_text(text, reply_markup=story_next_keyboard("story_ch1_done"))
    await callback.answer()


async def ch1_done(callback: CallbackQuery):
    text = (
        "📖 ГЛАВА 1 • ПРОЛОГ ЗАВЕРШЁН\n"
        "─────────────────────\n\n"
        "Ты вышел из кабинета с конвертом в руках.\n\n"
        "Что дальше?\n\n"
        "• Собрать состав\n"
        "• Открыть стартовый пак\n"
        "• Провести первый матч\n\n"
        "Глава продолжится после 5-го тура "
        "регулярного сезона."
    )
    await callback.message.edit_text(text, reply_markup=story_next_keyboard("back_to_menu", "⬅️ В меню"))
    await callback.answer()


def register_handlers(dp):
    dp.callback_query.register(show_story, F.data == "menu_story")
    dp.callback_query.register(start_ch1, F.data == "story_start_ch1")
    dp.callback_query.register(answer_yes, F.data == "story_ch1_answer_yes")
    dp.callback_query.register(answer_ask, F.data == "story_ch1_answer_ask")
    dp.callback_query.register(answer_why, F.data == "story_ch1_answer_why")
    dp.callback_query.register(after_ask, F.data == "story_ch1_after_ask")
    dp.callback_query.register(after_why, F.data == "story_ch1_after_why")
    dp.callback_query.register(ch1_done, F.data == "story_ch1_done")
