from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime

db = SQLAlchemy()

class Users(db.model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    interests = db.Column(db.String(250), nullable=False)
    clubs = db.Column(db.String(120), nullable=False)

    def init(self, username, first_name, last_name, email, interests, clubs):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.interests = interests
        self.clubs = clubs

class Clubs(db.model):

    __tablename__ = 'clubs'

    club_id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(50), unique=True, nullable=False)
    club_description = db.Column(db.String(250), nullable=False)
    club_president = db.Column(db.String(120), nullable=False)
    club_email = db.Column(db.String(120), unique=True, nullable=False)
    club_interests = db.Column(db.String(120), nullable=False)
    club_members = db.Column(db.String(250), nullable=False)

    def init(self, club_name, club_description, club_president, club_email, club_tags, club_members):
        self.club_name = club_name
        self.club_description = club_description
        self.club_president = club_president
        self.club_email = club_email
        self.club_tags = club_tags
        self.club_members = club_members

class Events(db.model):

    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_description = db.Column(db.String(250), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.DateTime, nullable=False)
    event_location = db.Column(db.String(120), nullable=False)
    event_club = db.Column(db.String(120), nullable=False)
    event_tags = db.Column(db.String(250), nullable=False)

    def init(self, event_name, event_description, event_date, event_time, event_location, event_club, event_tags):
        self.event_name = event_name
        self.event_description = event_description
        self.event_date = event_date
        self.event_time = event_time
        self.event_location = event_location
        self.event_club = event_club
        self.event_tags = event_tags



