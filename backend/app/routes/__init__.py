from operator import and_
from app import app
from app.db.session import Session
from app.db.models import Club, Event, User, Comment

from flask import Blueprint, abort, jsonify, request

from app.routes.authorize import login_required

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
    my_list = list(club_name)
    
    conditions = []
    for letter in my_list:
       conditions.append(Club.name.ilike(f"%{letter}%"))
        
    #clubs = session.query(Club).filter(and_(*conditions)).all()
    clubs = session.query(Club).filter(Club.name.ilike(f"%{club_name}%")).all()
    
    if not clubs:  # Check if the list is empty
        print(f"No clubs found for the name: {club_name}")
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
        'users': [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name
            } for user in club.users
        ]
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
    if not club:
        return jsonify({'error': 'Club not found'}), 404  # Handle club not found
    club.name = data['club_name']
    club.description = data['club_description']
    session.commit()
    return jsonify({
        'club_name': club.name,
        'club_description': club.description
    })

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

@app.route('/b/clubs/<int:club_id>/comments/<int:comment_id>/delete', methods=['DELETE'])
def delete_comment(club_id, comment_id):  
    session = Session()
    comment = session.query(Comment).filter(Comment.comment_id == comment_id, Comment.club_id == club_id).first()  
    if comment:
        session.delete(comment)
        session.commit()
        return jsonify({"message": "Comment deleted successfully"})
    else:
        return jsonify({"error": "Comment not found"}), 404


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
    new_user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'], grad_year=2024, interests=data['interests'], bio=data['bio'])
    session.add(new_user)
    session.commit()
    return jsonify(new_user)

@app.route('/b/users', methods=['GET'])
def get_all_users():
    users = Session().query(User).all()
    return jsonify([
        {
            'id': user.id,
            'email': user.email,
            'password_pash': user.password_hash,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'grad_year': user.grad_year,
            'interests': user.interests,
            'bio': user.bio,
            'is_active': user.is_active,
        } for user in users
    ])

@app.route('/b/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Session().query(User).get(user_id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'password_pash': user.password_hash,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'grad_year': user.grad_year,
        'interests': user.interests,
        'bio': user.bio,
        'is_active': user.is_active,
    })

@app.route('/b/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return jsonify(user)

@login_required
@app.route('/b/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = Session()
    data = request.get_json()
    print(data)
    user = session.query(User).get(user_id)
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.grad_year = data['grad_year']
    user.interests = data['interests']
    user.bio = data['bio']
    session.commit()
    return jsonify({
        'id': user.id,
        'email': user.email,
        'password_pash': user.password_hash,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'grad_year': user.grad_year,
        'interests': user.interests,
        'bio': user.bio,
        'is_active': user.is_active,
    })

@app.route('/b/users/<int:user_id>/add-to-club/<int:club_id>', methods=['POST'])
def add_user_to_club(user_id, club_id):
    session = Session()
    user = session.query(User).get(user_id)
    club = session.query(Club).get(club_id)
    user.clubs.append(club)
    session.commit()
    return jsonify({
        'id': user.id,
        'email': user.email,
        'password_pash': user.password_hash,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'grad_year': user.grad_year,
        'interests': user.interests,
        'bio': user.bio,
        'is_active': user.is_active,
    })

@app.route('/b/users/<int:user_id>/clubs', methods=['GET'])
def get_clubs_for_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    return jsonify([
        {
            'id': club.id,
            'club_name': club.name,
            'club_description': club.description,
        } for club in user.clubs
    ])

import app.routes.authorize
