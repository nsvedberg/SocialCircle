from app.db.session import Session
from typing import Optional, List
from sqlalchemy import Table, Column, DateTime, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from argon2 import PasswordHasher
from dataclasses import dataclass
from datetime import datetime

class Model(DeclarativeBase):
    """The base model class. All models should inherit this class."""
    pass

# Join table for the many-to-many relationship between GroupChat and User
groupchat_members = Table(
    "groupchat_members",
    Model.metadata,
    Column("groupchat_id", ForeignKey("groupchat.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True)
)

@dataclass
class User(Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[Optional[str]]
    first_name: Mapped[str]
    last_name: Mapped[str]
    interests: Mapped[str]
    bio: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    # Many-to-many relationship to group chats
    groupchats: Mapped[List["GroupChat"]] = relationship(
        "GroupChat",
        secondary="groupchat_members",
        back_populates="users"
    )

    def __init__(self, email, first_name, last_name, interests):
        self.email = email
        self.password_hash = None
        self.first_name = first_name
        self.last_name = last_name
        self.interests = interests
        self.is_active = True

    @staticmethod
    def get_by_email(email):
        """Get a user by email."""
        session = Session()
        return session.scalars(select(User).filter_by(email=email)).first()

    def check_password(self, pw):
        """Check if the provided password matches the user's password."""
        ph = PasswordHasher()
        return ph.verify(self.password_hash, pw)

    def set_password(self, pw):
        """Hash and set the user's password."""
        ph = PasswordHasher()
        self.password_hash = ph.hash(pw)

@dataclass
class Club(Model):
    __tablename__ = 'club'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]

    # One-to-one or one-to-many relationship to GroupChat
    groupchat: Mapped["GroupChat"] = relationship("GroupChat", back_populates="club", uselist=False)
    
    # Relationship to comments
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="club", cascade="all, delete-orphan"
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description

@dataclass
class GroupChat(Model):
    __tablename__ = 'groupchat'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("club.id"))

    # Relationship to Club
    club: Mapped["Club"] = relationship("Club", back_populates="groupchat")

    # Many-to-many relationship to Users
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="groupchat_members",
        back_populates="groupchats"
    )

@dataclass
class Event(Model):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    event_name: Mapped[str] = mapped_column(String(255), nullable=False)
    event_description: Mapped[str] = mapped_column(String(500), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event_time: Mapped[str] = mapped_column(String(10), nullable=False)
    event_location: Mapped[str] = mapped_column(String(255), nullable=False)
    event_club: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    event_tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __init__(self, event_name, event_description, event_date, event_time, event_location, event_club=None, event_tags=None):
        self.event_name = event_name
        self.event_description = event_description
        self.event_date = event_date
        self.event_time = event_time
        self.event_location = event_location
        self.event_club = event_club
        self.event_tags = event_tags

@dataclass
class Comment(Model):
    __tablename__ = 'comments'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[str]
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('club.id'))

    # Relationship to Club
    club: Mapped["Club"] = relationship("Club", back_populates='comments')

    def __init__(self, comment, club_id):
        self.comment = comment
        self.club_id = club_id
