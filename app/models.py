from typing import Optional, List
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Text, ForeignKey
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

    decks: Mapped[List["Deck"]] = relationship(back_populates="user", cascade="all, delete-orphan")

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
