from operator import and_
from app import app
from app.db.session import Session
from app.db.models import Club, Event, User, Comment, Message

from flask import Blueprint, abort, jsonify, request

from app.routes.authorize import login_required

router = Blueprint('user', __name__, url_prefix='/user')

@app.route('/b/clubs/new', methods=['POST'])
def create_club():
    session = Session()
    data = request.get_json()
    new_club = Club(name=data['club_name'],
                    description=data['club_description'],
                    email=data['club_email'])
    session.add(new_club)
    creator = session.query(User).get(data['club_creator']['id'])
    new_club.users.append(creator) 
    session.commit()
    return jsonify({
        'id': new_club.id,  # Now we get get id for testing
        'club_name': new_club.name,
        'club_description': new_club.description,
        'club_email': new_club.email
    }), 201

@app.route('/b/clubs', methods=['GET'])
def get_all_clubs():
    clubs = Session().query(Club).all()
    return jsonify([
        {
            'id': club.id,
            'club_name': club.name,
            'club_description': club.description,
            'club_email': club.email,
            'users': [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name
            } for user in club.users
            ]
        } for club in clubs
    ])

@app.route('/b/clubs/<string:attribute>/<string:search_term>', methods=['GET'])
def search_club_by_attribute(attribute, search_term):
    session = Session()
    
    if attribute == 'name':
        clubs = session.query(Club).filter(Club.name.ilike(f"%{search_term}%")).all()
    elif attribute == 'id':
        clubs = session.query(Club).filter(Club.id == int(search_term)).all()
    elif attribute == 'description':
        clubs = session.query(Club).filter(Club.description.ilike(f"%{search_term}%")).all()
    else:
        return jsonify({'error': 'Invalid search attribute'}), 400
    
    if not clubs:
        return jsonify({'error': 'No clubs found'}), 404

    club_list = [{
        'id': club.id,
        'club_name': club.name,
        'club_description': club.description,
    } for club in clubs]
    
    return jsonify(club_list)

@app.route('/b/events/name/<string:attribute>/<string:search_term>', methods=['GET'])
def get_event_by_name(attribute, search_term):
    session = Session()
    if attribute == 'name':
        events = session.query(Event).filter(Event.event_name.ilike(f"%{search_term}%")).all()
    elif attribute == 'id':
        events = session.query(Event).filter(Event.id == int(search_term)).all()
    elif attribute == 'description':
        events = session.query(Event).filter(Event.event_description.ilike(f"%{search_term}%")).all()
    elif attribute == 'location':
        events = session.query(Event).filter(Event.event_location.ilike(f"%{search_term}%")).all()
    else:
        return jsonify({'error': 'Invalid search attribute'}), 400
    
    if not events:  # Check if the list is empty
        print(f"No events found for the name: {search_term}")
        return jsonify({'error': 'Event not found'}), 404


    # Create a list of dictionaries for each club found
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'event_name': event.event_name,
            'event_description': event.event_description,
            'event_location' : event.event_location,
        })
    
    return jsonify(event_list)
    

@app.route('/b/clubs/<int:club_id>', methods=['GET'])
def get_club(club_id):
    session = Session()
    club = session.query(Club).get(club_id)
    club_dict = {
        'id': club.id,
        'club_name': club.name,
        'club_description': club.description,
        'club_email': club.email,
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
    club.email = data['club_email']
    session.commit()
    return jsonify({
        'club_name': club.name,
        'club_description': club.description,
        'club_email': club.email,
    })

@app.route('/b/clubs/<int:club_id>/comments', methods=['POST'])
def add_comment(club_id):
    session = Session()
    data = request.get_json()
    comment_text = data.get('comment')
    creator_id = data.get('creator_id')
    club = session.query(Club).get(club_id)
    if club is not None:
        new_comment = Comment(comment=comment_text, club_id=club_id, creator_id=creator_id) 
        session.add(new_comment)
        session.commit()
        return {'comment_id': new_comment.comment_id, 
                'comment': new_comment.comment, 
                'creator_id': new_comment.creator_id, 
                'user': {
                    'id' : new_comment.user.id,
                    'first_name': new_comment.user.first_name,
                    'last_name': new_comment.user.last_name,
                }
        }, 201
    return {'error': 'Club not found'}, 404

@app.route('/b/clubs/<int:club_id>/comments', methods=['GET'])
def get_comments(club_id):
    session = Session()
    comments = session.query(Comment).filter(Comment.club_id == club_id).all()
    return [
        {
            'comment_id': comment.comment_id,
            'comment': comment.comment,
            'creator_id': comment.creator_id,
            'user': {
                'id' : comment.user.id,
                'first_name': comment.user.first_name,
                'last_name': comment.user.last_name,
            }
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
    return jsonify({ # Explicitly return so I can add id for testing purposes
        'id': new_event.id, # added id
        'event_name': new_event.event_name,
        'event_description': new_event.event_description,
        'event_date': new_event.event_date,
        'event_time': new_event.event_time,
        'event_location': new_event.event_location,
        'event_club': new_event.event_club,
        'event_tags': new_event.event_tags,
    }), 201

@app.route('/b/events', methods=['GET'])
def get_events():
    events = Session().query(Event).all()
    return jsonify([
        {
            'id': event.id,
            'event_name': event.event_name,
            'event_description': event.event_description,
            'event_date': event.event_date.isoformat(),
            'event_time': event.event_time,
            'event_location': event.event_location,
            'event_club': event.event_club,
            'event_tags': event.event_tags,
            'users': [
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                } for user in event.users
            ]
        } for event in events
    ])

@app.route('/b/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    session = Session()
    event = session.query(Event).get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    return jsonify({
        'id': event.id,
        'event_name': event.event_name,
        'event_description': event.event_description,
        'event_date': event.event_date.isoformat(),
        'event_time': event.event_time,
        'event_location': event.event_location,
        'event_club': event.event_club,
        'event_tags': event.event_tags,
        'users': [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name
            } for user in event.users
        ]  
    })

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
    if not event:
        return jsonify({'error': 'Event not found'}), 404  # Handle event not found
    event.event_name = data['event_name']
    event.event_description = data['event_description']
    event.event_date = data['event_date']
    event.event_time = data['event_time']
    event.event_location = data['event_location']
    session.commit()
    return jsonify(event)

#add in RSVP logic here!
@app.route('/b/events/<int:event_id>/rsvp', methods=['POST'])
def add_user_to_rsvp(event_id):
    session = Session()
    data = request.get_json()
    user_id = data.get('user_id')
    user = session.query(User).get(user_id)
    event = session.query(Event).get(event_id)
    if not user or not event:
        return jsonify({'error': 'User or Event not found'}), 404
    user.events.append(event)
    session.commit()
    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'grad_year': user.grad_year,
        'interests': user.interests,
        'bio': user.bio,
        'is_active': user.is_active,
    })

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

@app.route('/b/users/<int:user_id>/remove-from-club/<int:club_id>', methods=['DELETE'])
def remove_user_from_club(user_id, club_id):
    session = Session()
    user = session.query(User).get(user_id)
    club = session.query(Club).get(club_id)
    user.clubs.remove(club) 
    #club.users.remove(user) # Optionally you can use this line instead of the one above, but not both, otherwise club_user_relationship will have two deletion attempts
    session.commit()
    return jsonify({
        'user_id': user.id,
        'club_id': club.id,
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

@app.route('/b/messages/<string:groupchat_name>/all_messages', methods=['GET'])
def get_all_messages(groupchat_name):
    session = Session()
    messages = session.query(Message).filter(Message.groupchat_name == groupchat_name).order_by(Message.created_at).all()
    return jsonify([
        {
            'id': message.id,
            'text': message.text,
            'user_id': message.user_id,  # Corrected attribute name
            'groupchat_name': message.groupchat_name,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        } for message in messages
    ])



# Route to add a new message
@app.route('/b/messages/<string:groupchat_name>/', methods=['POST'])
def add_message(groupchat_name):
    session = Session()
    data = request.get_json()

    if not data or 'text' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    new_message = Message(
        text=data['text'],
        user_id=data['user_id'],  # Include user_id
        groupchat_name=groupchat_name,
    )
    session.add(new_message)
    session.commit()

    return jsonify({
        'id': new_message.id,
        'text': new_message.text,
        'user_id': new_message.user_id,
        'groupchat_name': new_message.groupchat_name,
        'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }), 201






import app.routes.authorize
