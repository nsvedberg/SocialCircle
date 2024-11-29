from __future__ import annotations

from app.db.session import Session

from typing import Optional, List


from argon2 import PasswordHasher

from dataclasses import dataclass

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime, Integer, String, select, ForeignKey
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Integer, String, select, ForeignKey
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import relationship

from typing import Optional, List

class Model(DeclarativeBase):
    """The base model class. All models should inherit this class."""

    pass

club_user_relationship = Table(
    "club_user_relationship",
    Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("club_id", ForeignKey("club.id")),
)

@dataclass
class User(Model):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[Optional[str]]

    first_name: Mapped[str]
    last_name: Mapped[str]

    grad_year: Mapped[int]

    interests: Mapped[str]
    bio: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)

    clubs: Mapped[List[Club]] = relationship(
        secondary=club_user_relationship, back_populates="users"
    )

    comments: Mapped[List[Comment]] = relationship("Comment", back_populates="user")

    def init(self, email, first_name, last_name, interests):
        self.email = email
        self.password_hash = None
        self.first_name = first_name
        self.last_name = last_name
        self.interests = interests
        self.is_active = True

    def get_by_email(email):
        """Get a user, given the email."""
        session = Session()
        return session.scalars(select(User).filter_by(email=email)).first()

    def check_password(self, pw):
        """Check that a password is correct for a user."""
        ph = PasswordHasher()
        return ph.verify(self.password_hash, pw)

    def set_password(self, pw):
        """Set the password for a user."""
        ph = PasswordHasher()
        self.password_hash = ph.hash(pw)

@dataclass
class Club(Model):

    __tablename__ = 'club'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str]
    description: Mapped[str]
    email: Mapped[str]

    users: Mapped[List[User]] = relationship(
        secondary=club_user_relationship, back_populates="clubs"
    )

    # TODO: relationship to user for president & other club admins
    # TODO: relationship to interests
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="club", cascade="all, delete-orphan") # This should delete all the comments when all clubs delelted

    def init(self, name, description):
        self.name = name
        self.description = description

@dataclass
class Event(Model):

    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    event_name: Mapped[str] = mapped_column(String(255), nullable=False)
    event_description: Mapped[str] = mapped_column(String(500), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Assuming time is handled as a string like "12:30 PM"
    event_time: Mapped[str] = mapped_column(String(10), nullable=False)
    
    event_location: Mapped[str] = mapped_column(String(255), nullable=False)

    # Can be optional if not supplied yet
    event_club: Mapped[str] = mapped_column(String(255), nullable=True)  

    # Assuming tags are a comma-separated string for now
    event_tags: Mapped[str] = mapped_column(String(255), nullable=True)  

    # TODO: relationship to club, tags, etc...

    def __init__(self, event_name, event_description, event_date, event_time,
                 event_location, event_club=None, event_tags=None):
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
    #user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('club.id'))
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    # Add similar relationships to the Club and User sections
    user = relationship("User", back_populates='comments')
    club = relationship("Club", back_populates='comments')
    
    def init(self, comment, club_id):
        self.comment = comment
        self.club_id = club_id
# Comment model, commented for now (ironic lol) until I can test it when the single club page is built
@dataclass
class Message(Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_user: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)