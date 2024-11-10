from operator import and_
from app import app
from app.db.session import Session
from app.db.models import Club, Event, EventSchema, User, Comment

from flask import Blueprint, abort, jsonify, request

from app.routes import user, club, event
from app.routes.authorize import login_required

@app.route('/b/events', methods=['GET'])
def get_events():
    events = Session().query(Event).all()
    schema = EventSchema()
    return schema.dump(events, many=True)

@app.route('/b/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Session().query(Event).get(event_id)
    schema = EventSchema()
    return schema.dump(event)

@login_required
@app.route('/b/events/new', methods=['POST'])
def create_event():
    session = Session()
    schema = EventSchema()
    data = request.get_json()
    new_event = schema.load(event)
    session.add(new_event)
    session.commit()
    return schema.dump(new_event)

@login_required
@app.route('/b/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    session = Session()
    schema = EventSchema()
    data = request.get_json()
    event = session.query(Event).get(event_id)
    schema.load(data, session=session, instance=event)
    session.commit()
    return schema.dump(new_event)

@login_required
@app.route('/b/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    session = Session()
    schema = EventSchema()
    event = session.query(Event).get(event_id)
    session.delete(event)
    session.commit()
    return schema.dump(event)
