"""
Functionality relating to initializing and connecting to the PostgreSQL database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as AlchemySession
from sqlalchemy.exc import IntegrityError
from os import getenv

# This is the database URL used to connect to the PostgreSQL database.
DATABASE_URL = getenv("DATABASE_URL")

# By using this file, we can create a launcher for connections to the database.
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10)


def init_db():
    """Create all of the required tables in the PostgreSQL database."""
    from db.models import Model

    Model.metadata.create_all(bind=engine)


class Session(AlchemySession):
    """A scoped connection to the database, which can run queries."""

    def __init__(self):
        super().__init__(engine)
