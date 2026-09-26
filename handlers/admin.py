from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database import async_session
from models import User, Card, UserCard, Match
from sqlalchemy import select, func, update

from keyboards.admin import (
    admin_main_keyboard, admin_players_keyboard, admin_economy_keyboard,
    admin_cards_keyboard, admin_story_keyboard, admin_moderation_keyboard,
    admin_system_keyboard, admin_back_keyboard
)


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


def guard(callback: CallbackQuery) -> bool:
    """Проверка прав."""
    if callback.from_user.id != ADMIN_ID:
        return False
    return True


# ─── ГЛАВНАЯ ПАНЕЛЬ ────────────────────────

async def cmd_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа.")
        return
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"🛡  GOD MODE\n"
        f"{line}\n\n"
        f"✅ Бот работает\n"
        f"✅ БД подключена\n"
        f"✅ Админ-доступ OK\n\n"
        f"Твой ID: {message.from_user.id}\n\n"
        f"{line}\n"
        f"Выбери раздел:"
    )
    await message.answer(text, reply_markup=admin_main_keyboard())


async def adm_back(callback: CallbackQuery):
    if not guard(callback):
        await callback.answer("⛔", show_alert=True)
        return
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"🛡  GOD MODE\n"
        f"{line}\n\n"
        f"Выбери раздел:"
    )
    await callback.message.edit_text(text, reply_markup=admin_main_keyboard())
    await callback.answer()


# ─── ИГРОКИ ────────────────────────────────

async def adm_players(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        total = await session.scalar(select(func.count(User.id)))
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"👤  ИГРОКИ\n"
        f"{line}\n\n"
        f"Всего в базе: {total or 0}\n\n"
        f"Выбери действие:"
    )
    await callback.message.edit_text(text, reply_markup=admin_players_keyboard())
    await callback.answer()


async def adm_self_pack(callback: CallbackQuery):
    if not guard(callback):
        return
    from services.card_service import give_starter_pack, format_card_short
    cards = await give_starter_pack(callback.from_user.id)
    cards_text = "\n".join([format_card_short(c) for c in cards]) if cards else "—"
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    await callback.message.edit_text(
        f"🎁  СТАРТОВЫЙ ПАК ВЫДАН\n"
        f"{line}\n"
        f"{cards_text}",
        reply_markup=admin_back_keyboard()
    )
    await callback.answer("Готово!")


async def adm_find_user(callback: CallbackQuery):
    if not guard(callback):
        return
    await callback.message.edit_text(
        "🔍  ПОИСК ИГРОКА\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Функция в разработке.\n\n"
        "Скоро: поиск по @username, "
        "просмотр профиля, "
        "редактирование ресурсов.",
        reply_markup=admin_back_keyboard()
    )
    await callback.answer()


# ─── ЭКОНОМИКА ─────────────────────────────

async def adm_economy(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
    coins = user.coins if user else 0
    rubies = user.rubies if user else 0
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"💰  ЭКОНОМИКА\n"
        f"{line}\n\n"
        f"Твой баланс:\n"
        f"💰 Монеты: {coins}\n"
        f"💎 Рубины: {rubies}\n\n"
        f"{line}\n"
        f"Выбери действие:"
    )
    await callback.message.edit_text(text, reply_markup=admin_economy_keyboard())
    await callback.answer()


async def adm_coins_10k(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.coins += 10000
            await session.commit()
    await callback.answer("💰 +10 000 монет!")


async def adm_coins_100k(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.coins += 100000
            await session.commit()
    await callback.answer("💰 +100 000 монет!")


async def adm_rubies_100(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.rubies += 100
            await session.commit()
    await callback.answer("💎 +100 рубинов!")


async def adm_rubies_1000(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.rubies += 1000
            await session.commit()
    await callback.answer("💎 +1000 рубинов!")


# ─── ЭНЕРГИЯ ───────────────────────────────

async def adm_energy(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.energy = 20
            await session.commit()
    await callback.answer("⚡ Энергия восстановлена!", show_alert=True)


# ─── КАРТОЧКИ ──────────────────────────────

async def adm_cards(callback: CallbackQuery):
    if not guard(callback):
        return
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"🃏  КАРТОЧКИ\n"
        f"{line}\n\n"
        f"Выбери действие:"
    )
    await callback.message.edit_text(text, reply_markup=admin_cards_keyboard())
    await callback.answer()


async def adm_give_legend(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        r = await session.execute(
            select(Card).where(Card.rarity == "legend").order_by(func.random()).limit(1)
        )
        card = r.scalar_one_or_none()
        if card:
            session.add(UserCard(user_id=callback.from_user.id, card_id=card.id))
            await session.commit()
            from services.card_service import format_card_short
            await callback.message.edit_text(
                f"👑 ЛЕГЕНДА ВЫДАНА\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{format_card_short(card)}",
                reply_markup=admin_back_keyboard()
            )
            await callback.answer("Выдано!")
        else:
            await callback.answer("Легенд в базе нет", show_alert=True)


async def adm_give_gold(callback: CallbackQuery):
    if not guard(callback):
        return
    from services.card_service import format_card_short
    async with async_session() as session:
        r = await session.execute(
            select(Card).where(Card.rarity == "gold").order_by(func.random()).limit(5)
        )
        cards = r.scalars().all()
        for c in cards:
            session.add(UserCard(user_id=callback.from_user.id, card_id=c.id))
        await session.commit()
        text = "\n".join([format_card_short(c) for c in cards])
    await callback.message.edit_text(
        f"🥇 ЗОЛОТЫЕ ВЫДАНЫ\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{text}",
        reply_markup=admin_back_keyboard()
    )
    await callback.answer("Готово!")


# ─── СЮЖЕТ ─────────────────────────────────

async def adm_story(callback: CallbackQuery):
    if not guard(callback):
        return
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"📖  СЮЖЕТ\n"
        f"{line}\n\n"
        f"Выбери действие:"
    )
    await callback.message.edit_text(text, reply_markup=admin_story_keyboard())
    await callback.answer()


async def adm_story_ch1(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.chapter = 1
            user.day = 1
            await session.commit()
    await callback.answer("📖 Глава 1 активирована")


async def adm_story_ch2(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.chapter = 2
            user.day = 1
            await session.commit()
    await callback.answer("📖 Глава 2 открыта")


async def adm_story_reset(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            user.chapter = 1
            user.day = 1
            user.story_scene = "start"
            await session.commit()
    await callback.answer("🔄 Сюжет сброшен")


# ─── СТАТИСТИКА ────────────────────────────

async def adm_stats(callback: CallbackQuery):
    if not guard(callback):
        return
    async with async_session() as session:
        users_count = await session.scalar(select(func.count(User.id)))
        cards_count = await session.scalar(select(func.count(Card.id)))
        user_cards_count = await session.scalar(select(func.count(UserCard.id)))
        matches_count = await session.scalar(select(func.count(Match.id)))

        # Топ-3 по монетам
        r = await session.execute(select(User).order_by(User.coins.desc()).limit(3))
        top_coins = r.scalars().all()

    line = "━━━━━━━━━━━━━━━━━━━━━━"
    top_text = ""
    for i, u in enumerate(top_coins, 1):
        top_text += f"{i}. {u.name or '?'} — {u.coins} 💰\n"

    text = (
        f"📊  СТАТИСТИКА БАЗЫ\n"
        f"{line}\n\n"
        f"👥 Игроков: {users_count or 0}\n"
        f"🃏 Карточек в базе: {cards_count or 0}\n"
        f"🎴 Карточек у игроков: {user_cards_count or 0}\n"
        f"🏒 Матчей: {matches_count or 0}\n\n"
        f"{line}\n"
        f"💰 ТОП-3 ПО МОНЕТАМ:\n"
        f"{top_text or '—'}\n"
        f"{line}"
    )
    await callback.message.edit_text(text, reply_markup=admin_back_keyboard())
    await callback.answer()


# ─── РАССЫЛКА ──────────────────────────────

async def adm_broadcast(callback: CallbackQuery):
    if not guard(callback):
        return
    await callback.message.edit_text(
        "📨  РАССЫЛКА\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Функция в разработке.\n\n"
        "Скоро: рассылка всем игрокам, "
        "по сегменту (уровень, клуб), "
        "отложенные сообщения.",
        reply_markup=admin_back_keyboard()
    )
    await callback.answer()


# ─── МОДЕРАЦИЯ ─────────────────────────────

async def adm_moderation(callback: CallbackQuery):
    if not guard(callback):
        return
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"🚫  МОДЕРАЦИЯ\n"
        f"{line}\n\n"
        f"Выбери действие:"
    )
    await callback.message.edit_text(text, reply_markup=admin_moderation_keyboard())
    await callback.answer()


async def adm_ban_user(callback: CallbackQuery):
    if not guard(callback):
        return
    await callback.answer("Функция в разработке", show_alert=True)


async def adm_unban_user(callback: CallbackQuery):
    if not guard(callback):
        return
    await callback.answer("Функция в разработке", show_alert=True)


# ─── БЭКАП ─────────────────────────────────

async def adm_backup(callback: CallbackQuery):
    if not guard(callback):
        return
    await callback.message.edit_text(
        "💾  БЭКАП\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Функция в разработке.\n\n"
        "Скоро: создание JSON-выгрузки "
        "всех данных игры, скачивание "
        "архива, восстановление из файла.",
        reply_markup=admin_back_keyboard()
    )
    await callback.answer()


# ─── СИСТЕМА ───────────────────────────────

async def adm_system(callback: CallbackQuery):
    if not guard(callback):
        return
    line = "━━━━━━━━━━━━━━━━━━━━━━"
    text = (
        f"⚙️  СИСТЕМА\n"
        f"{line}\n\n"
        f"Выбери действие:"
    )
    await callback.message.edit_text(text, reply_markup=admin_system_keyboard())
    await callback.answer()


async def adm_restart(callback: CallbackQuery):
    if not guard(callback):
        return
    await callback.answer("🔄 Перезапуск через деплой", show_alert=True)


async def adm_db_check(callback: CallbackQuery):
    if not guard(callback):
        return
    try:
        async with async_session() as session:
            await session.execute(select(func.count(User.id)))
        await callback.answer("✅ БД работает", show_alert=True)
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {e}", show_alert=True)


# ─── РЕГИСТРАЦИЯ ───────────────────────────

def register_handlers(dp):
    dp.message.register(cmd_admin, Command("admin"))

    dp.callback_query.register(adm_back, F.data == "adm_back")

    # Игроки
    dp.callback_query.register(adm_players, F.data == "adm_players")
    dp.callback_query.register(adm_self_pack, F.data == "adm_self_pack")
    dp.callback_query.register(adm_find_user, F.data == "adm_find_user")

    # Экономика
    dp.callback_query.register(adm_economy, F.data == "adm_economy")
    dp.callback_query.register(adm_coins_10k, F.data == "adm_coins_10k")
    dp.callback_query.register(adm_coins_100k, F.data == "adm_coins_100k")
    dp.callback_query.register(adm_rubies_100, F.data == "adm_rubies_100")
    dp.callback_query.register(adm_rubies_1000, F.data == "adm_rubies_1000")

    # Энергия
    dp.callback_query.register(adm_energy, F.data == "adm_energy")

    # Карточки
    dp.callback_query.register(adm_cards, F.data == "adm_cards")
    dp.callback_query.register(adm_give_legend, F.data == "adm_give_legend")
    dp.callback_query.register(adm_give_gold, F.data == "adm_give_gold")

    # Сюжет
    dp.callback_query.register(adm_story, F.data == "adm_story")
    dp.callback_query.register(adm_story_ch1, F.data == "adm_story_ch1")
    dp.callback_query.register(adm_story_ch2, F.data == "adm_story_ch2")
    dp.callback_query.register(adm_story_reset, F.data == "adm_story_reset")

    # Статистика
    dp.callback_query.register(adm_stats, F.data == "adm_stats")

    # Рассылка
    dp.callback_query.register(adm_broadcast, F.data == "adm_broadcast")

    # Модерация
    dp.callback_query.register(adm_moderation, F.data == "adm_moderation")
    dp.callback_query.register(adm_ban_user, F.data == "adm_ban_user")
    dp.callback_query.register(adm_unban_user, F.data == "adm_unban_user")

    # Бэкап
    dp.callback_query.register(adm_backup, F.data == "adm_backup")

    # Система
    dp.callback_query.register(adm_system, F.data == "adm_system")
    dp.callback_query.register(adm_restart, F.data == "adm_restart")
    dp.callback_query.register(adm_db_check, F.data == "adm_db_check")
