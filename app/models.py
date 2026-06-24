from typing import Optional, List
from datetime import datetime, timezone, date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Text, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(64), default='fa-user', server_default='fa-user')
    
    current_streak: Mapped[int] = mapped_column(default=0, server_default='0')
    last_activity_date: Mapped[Optional[date]] = mapped_column(Date, default=None, nullable=True)
    daily_target: Mapped[int] = mapped_column(default=10, server_default='10')
    daily_progress: Mapped[int] = mapped_column(default=0, server_default='0')

    decks: Mapped[List["Deck"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    scores: Mapped[List["Score"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def record_activity(self, points: int):
        from datetime import date as dt_date, timedelta
        today = dt_date.today()
        
        if self.last_activity_date is None:
            self.current_streak = 1
            self.daily_progress = points
        elif self.last_activity_date == today:
            self.daily_progress += points
        elif self.last_activity_date == today - timedelta(days=1):
            self.current_streak += 1
            self.daily_progress = points
        else:
            self.current_streak = 1
            self.daily_progress = points
            
        self.last_activity_date = today

    def get_daily_progress(self) -> int:
        from datetime import date as dt_date
        if self.last_activity_date != dt_date.today():
            return 0
        return self.daily_progress

    @property
    def streak(self) -> int:
        from datetime import date as dt_date, timedelta
        if self.last_activity_date is None:
            return 0
        today = dt_date.today()
        if self.last_activity_date == today or self.last_activity_date == today - timedelta(days=1):
            return self.current_streak
        return 0

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Deck(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    deck_type: Mapped[str] = mapped_column(String(64), default='standard', server_default='standard')

    user: Mapped["User"] = relationship(back_populates="decks")
    cards: Mapped[List["Card"]] = relationship(back_populates="deck", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Deck {self.name}>"

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(128))
    meaning: Mapped[str] = mapped_column(String(256))
    example_sentence: Mapped[Optional[str]] = mapped_column(Text)
    deck_id: Mapped[int] = mapped_column(ForeignKey('deck.id'))

    deck: Mapped["Deck"] = relationship(back_populates="cards")

    def __repr__(self) -> str:
        return f"<Card {self.word}>"


class Score(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    game_name: Mapped[str] = mapped_column(String(64))
    score: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="scores")

    def __repr__(self) -> str:
        return f"<Score {self.game_name}: {self.score} by User {self.user_id}>"


class CurriculumUnit(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    unit_number: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column(String(128))
    grammar_topic: Mapped[str] = mapped_column(String(128))
    grammar_explanation: Mapped[str] = mapped_column(Text)
    words_description: Mapped[str] = mapped_column(String(256))

    def __repr__(self) -> str:
        return f"<CurriculumUnit Unit {self.unit_number}: {self.title}>"
