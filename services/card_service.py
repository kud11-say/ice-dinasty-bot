from sqlalchemy import select, func
from database import async_session
from models import Card, UserCard
from data.clubs import club_emoji


RARITY_EMOJI = {"bronze": "🥉", "silver": "🥈", "gold": "🥇",
                "elite": "💎", "legend": "👑", "icon": "🌟"}
RARITY_LABEL = {"bronze": "БРОНЗА", "silver": "СЕРЕБРО", "gold": "ЗОЛОТО",
                "elite": "ЭЛИТА", "legend": "ЛЕГЕНДА", "icon": "ИКОНА"}
POSITION_EMOJI = {"ЦН": "🎯", "ЛП": "⚡", "ПП": "⚡", "З": "🛡", "В": "🧤"}
ROLE_RU = {
    "sniper": "Снайпер", "playmaker": "Плеймейкер", "speedster": "Скороход",
    "defender": "Домосед", "universal": "Универсал", "wall": "Стена",
    "flexible": "Гибкий",
}
FORM_EMOJI = {"hot": "🔥", "normal": "🙂", "cold": "❄️"}
COUNTRY_FLAG = {
    "Россия": "🇷🇺", "Канада": "🇨🇦", "США": "🇺🇸", "Швеция": "🇸🇪",
    "Финляндия": "🇫🇮", "Чехия": "🇨🇿", "Словакия": "🇸🇰",
}


def format_card_short(card) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    return f"{rarity} {pos} {card.name} ({card.ovr})"


def format_card_full(card, stars: int = 0, form: str = "normal", injury: int = 0) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    label = RARITY_LABEL.get(card.rarity, "?")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    role = ROLE_RU.get(card.role, card.role)
    stars_str = "⭐" * stars + "☆" * (5 - stars)
    form_em = FORM_EMOJI.get(form, "🙂")
    club_em = club_emoji(card.club or "")
    flag = COUNTRY_FLAG.get(card.country, "🏳️")
    line = "━━━━━━━━━━━━━━━━━━━━━━"

    text = (
        f"{line}\n"
        f"{rarity}  {label}\n"
        f"{line}\n"
        f"{pos}  {card.name.upper()}\n"
        f"    {card.position} • {card.age} лет\n"
        f"{line}\n"
        f"OVR: {card.ovr}\n"
        f"⚡{card.speed}  🎯{card.shot}  🎩{card.pass_}\n"
        f"🛡{card.defense}  💪{card.physical}"
    )
    if card.position == "В":
        text += f"  🧤{card.goalie}"
    text += (
        f"\n{line}\n"
        f"{flag} {card.country}\n"
        f"🏒 {card.league}  •  {club_em} {card.club}\n"
        f"🎭 Роль: {role}\n"
        f"{stars_str}  {form_em}"
    )
    if injury > 0:
        text += f"\n🩹 Травма: {injury} матчей"
    text += f"\n{line}"
    return text


async def give_starter_pack(user_id: int) -> list:
    """Выдать стартовый пак из 6 карточек."""
    async with async_session() as session:
        cards = []

        # 1. Капитан — ЦН 78–85
        r = await session.execute(
            select(Card).where(Card.position == "ЦН", Card.ovr >= 78, Card.ovr <= 85)
            .order_by(func.random()).limit(1)
        )
        c = r.scalar_one_or_none()
        if c: cards.append(c)

        # 2. Второй ЦН (для 2-го звена) 68–78
        r = await session.execute(
            select(Card).where(Card.position == "ЦН", Card.ovr >= 68, Card.ovr <= 78)
            .order_by(func.random()).limit(1)
        )
        c = r.scalar_one_or_none()
        if c: cards.append(c)

        # 3–4. Два крайних нападающих
        r = await session.execute(
            select(Card).where(Card.position.in_(["ЛП", "ПП"]), Card.ovr >= 68, Card.ovr <= 80)
            .order_by(func.random()).limit(2)
        )
        for c in r.scalars().all():
            cards.append(c)

        # 5. Защитник
        r = await session.execute(
            select(Card).where(Card.position == "З", Card.ovr >= 68, Card.ovr <= 80)
            .order_by(func.random()).limit(1)
        )
        c = r.scalar_one_or_none()
        if c: cards.append(c)

        # 6. Вратарь
        r = await session.execute(
            select(Card).where(Card.position == "В", Card.ovr >= 65, Card.ovr <= 80)
            .order_by(func.random()).limit(1)
        )
        c = r.scalar_one_or_none()
        if c: cards.append(c)

        for card in cards:
            session.add(UserCard(user_id=user_id, card_id=card.id))
        await session.commit()
        return cards


async def get_user_cards(user_id: int) -> list:
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id)
            .where(UserCard.user_id == user_id).order_by(Card.ovr.desc())
        )
        return [{"user_card": uc, "card": c} for uc, c in result.all()]


async def get_user_card_by_id(user_card_id: int, user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id)
            .where(UserCard.id == user_card_id, UserCard.user_id == user_id)
        )
        row = result.first()
        if row:
            return {"user_card": row[0], "card": row[1]}
        return None
