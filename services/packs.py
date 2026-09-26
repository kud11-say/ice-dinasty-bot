import random
from sqlalchemy import select, func
from database import async_session
from models import Card, UserCard, User


PACKS = {
    "bronze": {"name": "Бронзовый", "price": 1000, "cards": 3, "emoji": "🥉", "min_ovr": 65},
    "silver": {"name": "Серебряный", "price": 5000, "cards": 5, "emoji": "🥈", "min_ovr": 72},
    "gold": {"name": "Золотой", "price": 15000, "cards": 5, "emoji": "🥇", "min_ovr": 78},
    "elite": {"name": "Элитный", "price": 50000, "cards": 3, "emoji": "💎", "min_ovr": 85},
}


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

        cards_got = []

        # Гарантированная карта нужного уровня
        r = await session.execute(
            select(Card).where(Card.ovr >= pack["min_ovr"])
            .order_by(func.random()).limit(1)
        )
        guarantee = r.scalar_one_or_none()
        if guarantee:
            cards_got.append(guarantee)

        # Остальные — случайные
        for _ in range(pack["cards"] - 1):
            r = await session.execute(select(Card).order_by(func.random()).limit(1))
            c = r.scalar_one_or_none()
            if c and c.id not in [x.id for x in cards_got]:
                cards_got.append(c)

        for card in cards_got:
            session.add(UserCard(user_id=user_id, card_id=card.id))

        await session.commit()
        return {"cards": cards_got, "price": pack["price"]}
