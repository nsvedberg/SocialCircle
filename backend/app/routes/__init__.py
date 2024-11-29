from operator import and_
from app import app
from app.db.session import Session
from app.db.models import Club, Event, User, Comment, Message

from flask import Blueprint, abort, jsonify, request

from app.routes.authorize import login_required

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
import app.routes.club
import app.routes.event
import app.routes.interest
import app.routes.user
