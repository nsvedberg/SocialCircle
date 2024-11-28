from __future__ import annotations

from app.db.session import Session

from typing import Optional, List

from argon2 import PasswordHasher

from dataclasses import dataclass

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Date, DateTime, Integer, String, select, ForeignKey
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Integer, String, select, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import relationship

from typing import Optional, List

from marshmallow import Schema, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Model(DeclarativeBase):
    """The base model class. All models should inherit this class."""

    pass

club_officer_relationship = Table(
    "club_officer_relationship",
    Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("club_id", ForeignKey("club.id")),
)

club_member_relationship = Table(
    "club_member_relationship",
    Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("club_id", ForeignKey("club.id")),
)

user_interest_relationship = Table(
    "user_interest_relationship",
    Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("interest_id", ForeignKey("interest.id")),
)

club_interest_relationship = Table(
    "club_interest_relationship",
    Model.metadata,
    Column("club_id", ForeignKey("club.id")),
    Column("interest_id", ForeignKey("interest.id")),
)

event_interest_relationship = Table(
    "event_interest_relationship",
    Model.metadata,
    Column("event_id", ForeignKey("event.id")),
    Column("interest_id", ForeignKey("interest.id")),
)

class Interest(Model):

    __tablename__ = 'interest'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]

class User(Model):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[Optional[str]]

    first_name: Mapped[str]
    last_name: Mapped[str]

    grad_year: Mapped[int]

    bio: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)

    officer_of: Mapped[List[Club]] = relationship(
        secondary=club_officer_relationship, back_populates="officers"
    )

    member_of: Mapped[List[Club]] = relationship(
        secondary=club_member_relationship, back_populates="members"
    )

    interests: Mapped[List[Interest]] = relationship(
        secondary=user_interest_relationship
    )

    comments: Mapped[List[Comment]] = relationship(back_populates="author")

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

class Club(Model):

    __tablename__ = 'club'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str]
    description: Mapped[str]
    email: Mapped[str]

    officers: Mapped[List[User]] = relationship(
        secondary=club_officer_relationship, back_populates="officer_of"
    )

    members: Mapped[List[User]] = relationship(
        secondary=club_member_relationship, back_populates="member_of"
    )

    interests: Mapped[List[Interest]] = relationship(
        secondary=club_interest_relationship
    )

    comments: Mapped[List["Comment"]] = relationship(back_populates="club")

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

    interests: Mapped[List[Interest]] = relationship(
        secondary=event_interest_relationship
    )

class Comment(Model):
    __tablename__ = 'comment'
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[str]

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship("User", back_populates='comments')

    club_id: Mapped[int] = mapped_column(ForeignKey("club.id"))
    club: Mapped[Club] = relationship("Club", back_populates='comments')

class InterestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Interest
        include_relationships = True
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

class ClubSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Club
        include_relationships = True
        load_instance = True

class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        include_relationships = True
        load_instance = True
