from app.db.session import Session

from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import Integer, String, select

from datetime import datetime

from argon2 import PasswordHasher

class Model(DeclarativeBase):
    """The base model class. All models should inherit this class."""

    pass

class User(Model):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[Optional[str]]

    first_name: Mapped[str]
    last_name: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)

    # TODO: relationship to interests & clubs

    def init(self, email, first_name, last_name):
        self.email = email
        self.password_hash = None
        self.first_name = first_name
        self.last_name = last_name
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

class Club(Model):

    __tablename__ = 'club'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str]
    description: Mapped[str]

    # TODO: relationship to user for president & other club admins
    # TODO: relationship to user for club members
    # TODO: relationship to interests

    def init(self, name, description):
        self.name = name
        self.description = description

class Event(Model):

    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]

    when: Mapped[datetime]
    location: Mapped[str]

    # TODO: relationship to club, tags, etc...

    def init(self, name, description, when, location):
        self.name = name
        self.description = description
        self.when = when
        self.description = description

# Comment model, commented for now (ironic lol) until I can test it when the single club page is built
'''
class Comment(Model):
    __tablename__ = 'comments'
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[str]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('club.id'))

    # Add similar relationships to the Club and User sections
    user = relationship("User", back_populates='comments')
    club = relationship("Club", back_populates='comments')
    
    def init(self, comment, user_id, club_id):
        self.comment = comment
        self.user_id = user_id
        self.club_id = club_id

'''