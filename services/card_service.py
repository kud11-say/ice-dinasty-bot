import random
from sqlalchemy import select, func
from database import async_session
from models import Card, UserCard


async def give_starter_pack(user_id: int) -> list:
    """Выдать стартовый пак из 5 карточек."""
    async with async_session() as session:
        # Берём карточки по одной из каждой категории
        cards = []
        
        # 1. Капитан — ЦН с OVR 78-84
        result = await session.execute(
            select(Card).where(
                Card.position == "ЦН",
                Card.ovr >= 78,
                Card.ovr <= 85
            ).order_by(func.random()).limit(1)
        )
        captain = result.scalar_one_or_none()
        if captain:
            cards.append(captain)
        
        # 2. ЛП или ПП с OVR 70-78
        result = await session.execute(
            select(Card).where(
                Card.position.in_(["ЛП", "ПП"]),
                Card.ovr >= 68,
                Card.ovr <= 78
            ).order_by(func.random()).limit(1)
        )
        winger = result.scalar_one_or_none()
        if winger:
            cards.append(winger)
        
        # 3. Второй крайний
        result = await session.execute(
            select(Card).where(
                Card.position.in_(["ЛП", "ПП"]),
                Card.ovr >= 68,
                Card.ovr <= 78
            ).order_by(func.random()).limit(1)
        )
        winger2 = result.scalar_one_or_none()
        if winger2 and winger2.id != winger.id:
            cards.append(winger2)
        
        # 4. Защитник
        result = await session.execute(
            select(Card).where(
                Card.position == "З",
                Card.ovr >= 68,
                Card.ovr <= 78
            ).order_by(func.random()).limit(1)
        )
        defender = result.scalar_one_or_none()
        if defender:
            cards.append(defender)
        
        # 5. Вратарь
        result = await session.execute(
            select(Card).where(
                Card.position == "В",
                Card.ovr >= 65,
                Card.ovr <= 78
            ).order_by(func.random()).limit(1)
        )
        goalie = result.scalar_one_or_none()
        if goalie:
            cards.append(goalie)
        
        # Выдаём игроку
        for card in cards:
            user_card = UserCard(user_id=user_id, card_id=card.id)
            session.add(user_card)
        
        await session.commit()
        
        return cards


async def get_user_cards(user_id: int) -> list:
    """Получить все карточки игрока с полной информацией."""
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id).where(UserCard.user_id == user_id)
        )
        rows = result.all()
        return [{"user_card": uc, "card": c} for uc, c in rows]


async def get_user_card_by_id(user_card_id: int, user_id: int):
    """Получить конкретную карточку игрока."""
    async with async_session() as session:
        result = await session.execute(
            select(UserCard, Card).join(Card, UserCard.card_id == Card.id).where(
                UserCard.id == user_card_id,
                UserCard.user_id == user_id
            )
        )
        row = result.first()
        if row:
            return {"user_card": row[0], "card": row[1]}
        return None
