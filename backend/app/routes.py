from app import app
from app.db.session import Session
from app.db.models import Clubs, Events, Users

from flask import Blueprint, abort, jsonify, request

router = Blueprint('user', __name__, url_prefix='/user')

@app.route('/')
def home():
    return "Hello, Flask!"

# @app.route('/user/clubs', methods=['GET'])
# def get_user_clubs():
#     data = request.get_json()
#     user = Users.query.filter_by(username=data['username']).first()
#     if user is None:
#         return abort(404)
#     return jsonify(user.clubs)

@app.route('/clubs/new', methods=['POST'])
def create_club():
    session = Session()
    data = request.get_json()
    new_club = Clubs(club_name=data['club_name'], club_description=data['club_description'], club_president=data['club_president'], club_email=data['club_email'], club_tags=data['club_tags'], club_members=data['club_members'])
    session.add(new_club)
    session.commit()
    return jsonify(new_club)

@app.route('/clubs', methods=['GET'])
def get_clubs():
    session = Session()
    clubs = session.query(Clubs).all()
    return jsonify(clubs)

@app.route('/clubs/<int:club_id>', methods=['GET'])
def get_club(club_id):
    session = Session()
    club = session.query(Clubs).get(club_id)
    return jsonify(club)

@app.route('/clubs/<int:club_id>', methods=['DELETE'])
def delete_club(club_id):
    session = Session()
    club = session.query(Clubs).get(club_id)
    session.delete(club)
    session.commit()
    return jsonify(club)


# commented out until we have the DB relationships finalized
# @app.route('/clubs/<int:club_id>', methods=['PUT'])
# def update_club(club_id):
#     session = Session()
#     data = request.get_json()
#     club = session.query(Clubs).get(club_id)
#     club.club_name = data['club_name']
#     club.club_description = data['club_description']
#     club.club_president = data['club_president']
#     club.club_email = data['club_email']
#     club.club_tags = data['club_tags']
#     club.club_members = data['club_members']
#     session.commit()
#     return jsonify(club)

@app.route('/events/new', methods=['POST'])
def create_event():
    session = Session()
    data = request.get_json()
    new_event = Events(event_name=data['event_name'], event_description=data['event_description'], event_date=data['event_date'], event_time=data['event_time'], event_location=data['event_location'], event_club=data['event_club'], event_tags=data['event_tags'])
    session.add(new_event)
    session.commit()
    return jsonify(new_event)


