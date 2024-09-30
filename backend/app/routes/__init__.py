from app import app
from app.db.session import Session
from app.db.models import Clubs, Events, Users

from flask import Blueprint, abort, jsonify, request

router = Blueprint('user', __name__, url_prefix='/user')

#needs to be updated when relationships are finalized in the database
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


#TODO update this route to reflect the final database relationships
@app.route('/clubs/<int:club_id>', methods=['PUT'])
def update_club(club_id):
    session = Session()
    data = request.get_json()
    club = session.query(Clubs).get(club_id)
    club.club_name = data['club_name']
    club.club_description = data['club_description']
    club.club_president = data['club_president']
    club.club_email = data['club_email']
    club.club_tags = data['club_tags']
    club.club_members = data['club_members']
    session.commit()
    return jsonify(club)

@app.route('/events/new', methods=['POST'])
def create_event():
    session = Session()
    data = request.get_json()
    new_event = Events(event_name=data['event_name'], event_description=data['event_description'], event_date=data['event_date'], event_time=data['event_time'], event_location=data['event_location'], event_club=data['event_club'], event_tags=data['event_tags'])
    session.add(new_event)
    session.commit()
    return jsonify(new_event)

@app.route('/events', methods=['GET'])
def get_events():
    session = Session()
    events = session.query(Events).all()
    return jsonify(events)

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    session = Session()
    event = session.query(Events).get(event_id)
    return jsonify(event)

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    session = Session()
    event = session.query(Events).get(event_id)
    session.delete(event)
    session.commit()
    return jsonify(event)

 #TODO: update this route to reflect the final database relationships
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    session = Session()
    data = request.get_json()
    event = session.query(Events).get(event_id)
    event.event_name = data['event_name']
    event.event_description = data['event_description']
    event.event_date = data['event_date']
    event.event_time = data['event_time']
    event.event_location = data['event_location']
    event.event_club = data['event_club']
    event.event_tags = data['event_tags']
    session.commit()
    return jsonify(event)

#TODO: update this route to reflect the final database relationships
@app.route('/users/new', methods=['POST'])
def create_user():
    session = Session()
    data = request.get_json()
    new_user = Users(user_name=data['user_name'], user_email=data['user_email'], user_clubs=data['user_clubs'], user_interests=data['user_interests'])
    session.add(new_user)
    session.commit()
    return jsonify(new_user)

@app.route('/users', methods=['GET'])
def get_users():
    session = Session()
    users = session.query(Users).all()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = Session()
    user = session.query(Users).get(user_id)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(Users).get(user_id)
    session.delete(user)
    session.commit()
    return jsonify(user)

#TODO: update this route to reflect the final database relationships
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = Session()
    data = request.get_json()
    user = session.query(Users).get(user_id)
    user.user_name = data['user_name']
    user.user_email = data['user_email']
    user.user_clubs = data['user_clubs']
    user.user_interests = data['user_interests']
    session.commit()
    return jsonify(user)
