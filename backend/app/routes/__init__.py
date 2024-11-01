from app import app
from app.db.session import Session
from app.db.models import Club, Event, User, Comment

from flask import Blueprint, abort, jsonify, request

router = Blueprint('user', __name__, url_prefix='/user')

@app.route('/b/clubs/new', methods=['POST'])
def create_club():
    session = Session()
    data = request.get_json()
    new_club = Club(name=data['club_name'],
                    description=data['club_description'])
    session.add(new_club)
    session.commit()
    return jsonify(new_club)

@app.route('/b/clubs', methods=['GET'])
def get_all_clubs():
    clubs = Session().query(Club).all()
    return jsonify([
        {
            'id': club.id,
            'club_name': club.name,
            'club_description': club.description,
        } for club in clubs
    ])

@app.route('/b/clubs/name/<string:club_name>', methods=['GET'])
def get_club_by_name(club_name):
    session = Session()
    # Query the club by name
    clubs = session.query(Club).filter(Club.name.like(f"%{club_name}%")).all()

    if not clubs:  # Check if the list is empty
        return jsonify({'error': 'Club not found'}), 404

    # Create a list of dictionaries for each club found
    club_list = []
    for club in clubs:
        club_list.append({
            'id': club.id,
            'club_name': club.name,
            'club_description': club.description,
        })

    return jsonify(club_list)


@app.route('/b/clubs/<int:club_id>', methods=['GET'])
def get_club(club_id):
    session = Session()
    club = session.query(Club).get(club_id)
    club_dict = {
        'id': club.id,
        'club_name': club.name,
        'club_description': club.description,
    }
    return jsonify(club_dict)

@app.route('/b/clubs/<int:club_id>', methods=['DELETE'])
def delete_club(club_id):
    session = Session()
    club = session.query(Club).get(club_id)
    club_dict = {
        'id': club.id,
        'club_name': club.name,
        'club_description': club.description,
    }
    session.delete(club)
    session.commit()
    return jsonify(club_dict)

@app.route('/b/clubs/<int:club_id>', methods=['PUT'])
def update_club(club_id):
    session = Session()
    data = request.get_json()
    club = session.query(Club).get(club_id)
    club.club_name = data['club_name']
    club.club_description = data['club_description']
    club.club_president = data['club_president']
    club.club_email = data['club_email']
    club.club_tags = data['club_tags']
    club.club_members = data['club_members']
    session.commit()
    return club

@app.route('/b/clubs/<int:club_id>/comments', methods=['POST'])
def add_comment(club_id):
    session = Session()
    data = request.get_json()
    comment_text = data.get('comment')
    club = session.query(Club).get(club_id)
    if club is not None:
        new_comment = Comment(comment=comment_text, club_id=club_id) 
        session.add(new_comment)
        session.commit()
        return {'comment_id': new_comment.comment_id, 'comment': new_comment.comment}, 201
    return {'error': 'Club not found'}, 404

@app.route('/b/clubs/<int:club_id>/comments', methods=['GET'])
def get_comments(club_id):
    session = Session()
    comments = session.query(Comment).filter(Comment.club_id == club_id).all()
    return [
        {
            'comment_id': comment.comment_id,
            'comment': comment.comment
        } for comment in comments
    ]

@app.route('/b/clubs/<int:club_id>/comments/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id, club_id):
    session = Session()
    comment = session.query(Comment).filter(Comment.comment_id == comment_id).first() # Getting the comment that matches the id wanted
    data = request.get_json()
    new_comment = data.get('comment')
    # "comment.comment" represents the text in the model, here we set the comment to the new one.
    comment.comment = new_comment
    session.commit()
    return jsonify({"comment_id": comment.comment_id, "comment": comment.comment})

@app.route('/b/events/new', methods=['POST'])
def create_event():
    session = Session()
    data = request.get_json()
    new_event = Event(event_name=data['event_name'],
                      event_description=data['event_description'],
                      event_date=data['event_date'],
                      event_time=data['event_time'],
                      event_location=data['event_location'],
                      event_club=data['event_club'],
                      event_tags=data['event_tags'])
    session.add(new_event)
    session.commit()
    return jsonify(new_event)

@app.route('/b/events', methods=['GET'])
def get_events():
    return Session().query(Event).all()

@app.route('/b/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Session().query(Event).get(event_id)
    return jsonify(event)

@app.route('/b/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    session = Session()
    event = session.query(Event).get(event_id)
    session.delete(event)
    session.commit()
    return jsonify(event)

@app.route('/b/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    session = Session()
    data = request.get_json()
    event = session.query(Event).get(event_id)
    event.event_name = data['event_name']
    event.event_description = data['event_description']
    event.event_date = data['event_date']
    event.event_time = data['event_time']
    event.event_location = data['event_location']
    event.event_club = data['event_club']
    event.event_tags = data['event_tags']
    session.commit()
    return jsonify(event)

@app.route('/b/users/new', methods=['POST'])
def create_user():
    session = Session()
    data = request.get_json()
    new_user = User(user_name=data['user_name'], user_email=data['user_email'], user_clubs=data['user_clubs'], user_interests=data['user_interests'])
    session.add(new_user)
    session.commit()
    return jsonify(new_user)

@app.route('/b/users', methods=['GET'])
def get_all_users():
    return Session().query(User).all()

@app.route('/b/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(Session().query(User).get(user_id))

@app.route('/b/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return jsonify(user)

@app.route('/b/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = Session()
    data = request.get_json()
    user = session.query(User).get(user_id)
    user.user_name = data['user_name']
    user.user_email = data['user_email']
    user.user_clubs = data['user_clubs']
    user.user_interests = data['user_interests']
    session.commit()
    return jsonify(user)

import app.routes.authorize
