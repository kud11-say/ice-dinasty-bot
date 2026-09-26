import random
from sqlalchemy import select, func
from database import async_session
from models import Card, UserCard, User
from services.card_service import format_card_short


PACKS = {
    "bronze": {"name": "Бронзовый", "price": 1000, "cards": 3, "emoji": "🥉", "min_rarity": 0},
    "silver": {"name": "Серебряный", "price": 5000, "cards": 5, "emoji": "🥈", "min_rarity": 1},
    "gold": {"name": "Золотой", "price": 15000, "cards": 5, "emoji": "🥇", "min_rarity": 2},
    "elite": {"name": "Элитный", "price": 50000, "cards": 3, "emoji": "💎", "min_rarity": 3},
}

RARITY_ORDER = {"bronze": 0, "silver": 1, "gold": 2, "elite": 3, "legend": 4, "icon": 5}


async def open_pack(user_id: int, pack_key: str) -> dict:
    pack = PACKS.get(pack_key)
    if not pack:
        return {"error": "unknown_pack"}

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return {"error": "no_user"}
        if user.coins < pack["price"]:
            return {"error": "not_enough_coins", "need": pack["price"], "have": user.coins}

        user.coins -= pack["price"]

        # Выбор карт
        cards_got = []
        min_r = pack["min_rarity"]
        # Гарантия — 1 карта с min_rarity или выше
        result = await session.execute(
            select(Card).where(Card.ovr >= 72 + min_r * 8).order_by(func.random()).limit(1)
        )
        guarantee = result.scalar_one_or_none()
        if guarantee:
            cards_got.append(guarantee)

        for _ in range(pack["cards"] - 1):
            result = await session.execute(select(Card).order_by(func.random()).limit(1))
            c = result.scalar_one_or_none()
            if c:
                cards_got.append(c)

        for card in cards_got:
            session.add(UserCard(user_id=user_id, card_id=card.id))

        await session.commit()

        return {"cards": cards_got, "price": pack["price"]}
