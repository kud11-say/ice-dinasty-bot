from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """Игрок (ГМ)."""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)  # Telegram ID
    username = Column(String(64), nullable=True)
    name = Column(String(32), nullable=True)  # Имя ГМ
    age = Column(Integer, default=25)
    origin = Column(String(32), default="player")  # player/analyst/business/graduate/journalist/foreigner
    club = Column(String(64), nullable=True)
    league = Column(String(16), nullable=True)  # VHL/KHL/NHL
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=5000)
    rubies = Column(Integer, default=10)
    energy = Column(Integer, default=20)
    energy_bought = Column(Integer, default=0)
    rep_fans = Column(Integer, default=3)
    rep_press = Column(Integer, default=3)
    rep_players = Column(Integer, default=3)
    rep_board = Column(Integer, default=3)
    chapter = Column(Integer, default=1)
    day = Column(Integer, default=1)
    is_registered = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Card(Base):
    """Базовая карточка игрока (шаблон)."""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    position = Column(String(4), nullable=False)  # ЦН/ЛП/ПП/З/В
    age = Column(Integer, nullable=False)
    ovr = Column(Integer, nullable=False)
    speed = Column(Integer, default=50)
    shot = Column(Integer, default=50)
    pass_ = Column("pass", Integer, default=50)
    defense = Column(Integer, default=50)
    physical = Column(Integer, default=50)
    goalie = Column(Integer, default=0)
    rarity = Column(String(16), default="bronze")  # bronze/silver/gold/elite/legend/icon
    role = Column(String(32), default="universal")
    country = Column(String(32), default="Россия")
    league = Column(String(16), default="VHL")
    club = Column(String(64), default="")
    potential = Column(Integer, default=80)
    is_exclusive = Column(Boolean, default=False)


class UserCard(Base):
    """Карточка, принадлежащая игроку."""
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    stars = Column(Integer, default=0)
    form = Column(String(8), default="normal")  # hot/normal/cold
    injury_matches = Column(Integer, default=0)
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())


class TeamSlot(Base):
    """Слот в составе команды."""
    __tablename__ = "team_slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    slot = Column(String(16), nullable=False)  # line1_c, line1_lw, pair1_ld, goalie1 ...
    user_card_id = Column(Integer, ForeignKey("user_cards.id"), nullable=True)
    is_captain = Column(Boolean, default=False)
    is_assistant = Column(Boolean, default=False)


class Match(Base):
    """История матчей."""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    opponent = Column(String(64), nullable=False)
    score_my = Column(Integer, default=0)
    score_opp = Column(Integer, default=0)
    result = Column(String(16), default="")  # win/loss/ot/bull
    is_playoff = Column(Boolean, default=False)
    best_player = Column(String(64), nullable=True)
    played_at = Column(DateTime(timezone=True), server_default=func.now())


class Transaction(Base):
    """Транзакции (монеты, рубины)."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False)  # buy/sell/reward/donate
    amount = Column(Integer, default=0)
    currency = Column(String(16), default="coins")  # coins/rubies
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StoryProgress(Base):
    """Прогресс в сюжете."""
    __tablename__ = "story_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, unique=True)
    chapter = Column(Integer, default=1)
    scene = Column(String(64), default="start")
    flags = Column(Text, default="{}")  # JSON
    choices = Column(Text, default="[]")  # JSON


class AdminLog(Base):
    """Логи действий админа."""
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(BigInteger, nullable=False)
    action = Column(String(64), nullable=False)
    target_id = Column(BigInteger, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
