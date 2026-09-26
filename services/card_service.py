from sqlalchemy import select, func
from database import async_session
from models import Card, UserCard
from data.clubs import club_emoji

RARITY_EMOJI = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "elite": "💎", "legend": "👑", "icon": "🌟"}
RARITY_LABEL = {"bronze": "БРОНЗА", "silver": "СЕРЕБРО", "gold": "ЗОЛОТО",
                "elite": "ЭЛИТА", "legend": "ЛЕГЕНДА", "icon": "ИКОНА"}
POSITION_EMOJI = {"ЦН": "🎯", "ЛП": "⚡", "ПП": "⚡", "З": "🛡", "В": "🧤"}
ROLE_RU = {
    "sniper": "Снайпер", "playmaker": "Плеймейкер", "speedster": "Скороход",
    "defender": "Домосед", "universal": "Универсал", "wall": "Стена",
    "flexible": "Гибкий",
}
FORM_EMOJI = {"hot": "🔥", "normal": "🙂", "cold": "❄️"}


def format_card_short(card) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    return f"{rarity} {pos} {card.name} ({card.ovr})"


def format_card_full(card, stars=0, form="normal", injury=0) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    label = RARITY_LABEL.get(card.rarity, "?")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    role = ROLE_RU.get(card.role, card.role)
    stars_str = "⭐" * stars + "☆" * (5 - stars)
    form_em = FORM_EMOJI.get(form, "🙂")
    club_em = club_emoji(card.club or "")

    # Обрезаем длинные строки
    def fit(s, width=26):
        s = str(s)
        if len(s) > width:
            s = s[:width - 1] + "…"
        return s.ljust(width)

    lines = [
        "╔════════════════════════════╗",
        f"║ {rarity} {fit(label, 23)}║",
        "╠════════════════════════════╣",
        f"║ {pos} {fit(card.name, 23)}║",
        f"║ {fit(f'{card.position} • {card.age} лет', 26)}║",
        "╠════════════════════════════╣",
        f"║ OVR: {fit(card.ovr, 20)}║",
        f"║ ⚡{card.speed} 🎯{card.shot} 🎩{card.pass_} 🛡{card.defense} 💪{card.physical}{'   ' if card.position != 'В' else ''}║",
    ]
    if card.position == "В":
        lines.append(f"║ 🧤{card.goalie:<3}{fit('', 21)}║")
    lines += [
        "╠════════════════════════════╣",
        f"║ 🌍 {fit(card.country, 23)}║",
        f"║ 🏒 {fit(f'{card.league} • {card.club}', 23)}║",
        f"║ {club_em} {fit(role, 22)}║",
        f"║ {stars_str} {form_em}{fit('', 18)}║",
    ]
    if injury > 0:
        lines.append(f"║ 🩹 Травма: {injury} матчей{' ' * 11}║")
    lines.append("╚════════════════════════════╝")
    return "\n".join(lines)


async def give_starter_pack(user_id: int) -> list:
    async with async_session() as session:
        cards = []
        result = await session.execute(select(Card).where(Card.position == "ЦН", Card.ovr >= 78, Card.ovr <= 85).order_by(func.random()).limit(1))
        c = result.scalar_one_or_none()
        if c: cards.append(c)
        result = await session.execute(select(Card).where(Card.position.in_(["ЛП", "ПП"]), Card.ovr >= 68, Card.ovr <= 78).order_by(func.random()).limit(2))
        for c in result.scalars().all():
            cards.append(c)
        result = await session.execute(select(Card).where(Card.position == "З", Card.ovr >= 68, Card.ovr <= 78).order_by(func.random()).limit(1))
        c = result.scalar_one_or_none()
        if c: cards.append(c)
        result = await session.execute(select(Card).where(Card.position == "В", Card.ovr >= 65, Card.ovr <= 78).order_by(func.random()).limit(1))
        c = result.scalar_one_or_none()
        if c: cards.append(c)
        for card in cards:
            session.add(UserCard(user_id=user_id, card_id=card.id))
        await session.commit()
        return cards


async def get_user_cards(user_id: int) -> list:
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id).where(UserCard.user_id == user_id).order_by(Card.ovr.desc())
        )
        return [{"user_card": uc, "card": c} for uc, c in result.all()]


async def get_user_card_by_id(user_card_id: int, user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id).where(
                UserCard.id == user_card_id, UserCard.user_id == user_id
            )
        )
        row = result.first()
        if row:
            return {"user_card": row[0], "card": row[1]}
        return None
