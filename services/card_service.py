from sqlalchemy import select, func
from database import async_session
from models import Card, UserCard


RARITY_EMOJI = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "elite": "💎", "legend": "👑", "icon": "🌟"}
POSITION_EMOJI = {"ЦН": "🎯", "ЛП": "⚡", "ПП": "⚡", "З": "🛡", "В": "🧤"}
ROLE_RU = {
    "sniper": "Снайпер", "playmaker": "Плеймейкер", "speedster": "Скороход",
    "defender": "Домосед", "universal": "Универсал", "wall": "Стена",
    "flexible": "Гибкий",
}


def format_card_short(card) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    return f"{rarity} {pos} {card.name} ({card.ovr})"


def format_card_full(card, stars=0, form="normal", injury=0) -> str:
    rarity = RARITY_EMOJI.get(card.rarity, "❓")
    pos = POSITION_EMOJI.get(card.position, "🏒")
    role = ROLE_RU.get(card.role, card.role)
    stars_str = "⭐" * stars + "☆" * (5 - stars)
    form_emoji = {"hot": "🔥", "normal": "🙂", "cold": "❄️"}.get(form, "🙂")

    text = (
        f"╔══════════════════════════╗\n"
        f"║  {rarity} {card.rarity.upper():<21} ║\n"
        f"╠══════════════════════════╣\n"
        f"║  {pos} {card.name[:20]:<21} ║\n"
        f"║  {card.position} • {card.age} лет{' ' * (13 - len(str(card.age)))}║\n"
        f"╠══════════════════════════╣\n"
        f"║  OVR: {card.ovr:<19}║\n"
        f"║  ⚡{card.speed:<3} 🎯{card.shot:<3} 🎩{card.pass_:<3} 🛡{card.defense:<3}  ║\n"
        f"║  💪{card.physical:<3}"
    )
    if card.position == "В":
        text += f" 🧤{card.goalie:<3}"
    else:
        text += " " * 8
    text += "     ║\n"
    text += (
        f"╠══════════════════════════╣\n"
        f"║  🌍 {card.country[:20]:<21}║\n"
        f"║  🏒 {card.league} • 🏛 {card.club[:14]:<14}║\n"
        f"║  🎭 {role[:21]:<21}║\n"
        f"║  {stars_str} {form_emoji}{' ' * 10}║\n"
    )
    if injury > 0:
        text += f"║  🩹 Травма: {injury} матчей{' ' * 8}║\n"
    text += "╚══════════════════════════╝"
    return text


async def give_starter_pack(user_id: int) -> list:
    async with async_session() as session:
        cards = []
        # Капитан ЦН
        result = await session.execute(select(Card).where(Card.position == "ЦН", Card.ovr >= 78, Card.ovr <= 85).order_by(func.random()).limit(1))
        c = result.scalar_one_or_none()
        if c: cards.append(c)

        # Крайние
        result = await session.execute(select(Card).where(Card.position.in_(["ЛП", "ПП"]), Card.ovr >= 68, Card.ovr <= 78).order_by(func.random()).limit(2))
        for c in result.scalars().all():
            cards.append(c)

        # Защитник
        result = await session.execute(select(Card).where(Card.position == "З", Card.ovr >= 68, Card.ovr <= 78).order_by(func.random()).limit(1))
        c = result.scalar_one_or_none()
        if c: cards.append(c)

        # Вратарь
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
