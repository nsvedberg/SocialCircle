from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from datetime import datetime

class Model(DeclarativeBase):
    """The base model class. All models should inherit this class."""

    pass

class Users(Model):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]

    # TODO: relationship to interests & clubs

    def init(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

class Clubs(Model):

    __tablename__ = 'clubs'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]

    # TODO: relationship to user for president & other club admins
    # TODO: relationship to user for club members
    # TODO: relationship to interests

    def init(self, name, description):
        self.name = name
        self.description = description

class Events(Model):

    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]

    when: Mapped[DateTime]
    location: String

    # TODO: relationship to club, tags, etc...

    def init(self, name, description, when, location):
        self.name = name
        self.description = description
        self.when = when
        self.description = description
