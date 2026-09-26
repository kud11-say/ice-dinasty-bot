from sqlalchemy import (
    Column, Integer, String, Boolean, BigInteger, DateTime, Text, ForeignKey
)
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), nullable=True)
    name = Column(String(32), nullable=True)
    age = Column(Integer, default=25)
    origin = Column(String(32), default="player")
    club = Column(String(64), nullable=True)
    league = Column(String(16), nullable=True)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=5000)
    rubies = Column(Integer, default=10)
    energy = Column(Integer, default=20)
    energy_bought = Column(Integer, default=0)
    budget = Column(Integer, default=500000)
    rep_fans = Column(Integer, default=3)
    rep_press = Column(Integer, default=3)
    rep_players = Column(Integer, default=3)
    rep_board = Column(Integer, default=3)
    chapter = Column(Integer, default=1)
    day = Column(Integer, default=1)
    story_scene = Column(String(64), default="start")
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ot_wins = Column(Integer, default=0)
    ot_losses = Column(Integer, default=0)
    is_registered = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    position = Column(String(4), nullable=False)
    age = Column(Integer, nullable=False)
    ovr = Column(Integer, nullable=False)
    speed = Column(Integer, default=50)
    shot = Column(Integer, default=50)
    pass_ = Column("pass", Integer, default=50)
    defense = Column(Integer, default=50)
    physical = Column(Integer, default=50)
    goalie = Column(Integer, default=0)
    rarity = Column(String(16), default="bronze")
    role = Column(String(32), default="universal")
    country = Column(String(32), default="Россия")
    league = Column(String(16), default="VHL")
    club = Column(String(64), default="")
    potential = Column(Integer, default=80)
    is_exclusive = Column(Boolean, default=False)


class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    stars = Column(Integer, default=0)
    form = Column(String(8), default="normal")
    injury_matches = Column(Integer, default=0)
    is_in_team = Column(Boolean, default=False)
    slot = Column(String(16), nullable=True)
    is_captain = Column(Boolean, default=False)
    is_assistant = Column(Boolean, default=False)
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    opponent = Column(String(64), nullable=False)
    score_my = Column(Integer, default=0)
    score_opp = Column(Integer, default=0)
    result = Column(String(16), default="")
    is_playoff = Column(Boolean, default=False)
    best_player = Column(String(64), nullable=True)
    played_at = Column(DateTime(timezone=True), server_default=func.now())


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False)
    amount = Column(Integer, default=0)
    currency = Column(String(16), default="coins")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StoryFlag(Base):
    __tablename__ = "story_flags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    flag_name = Column(String(64), nullable=False)
    flag_value = Column(String(64), default="true")
