from operator import and_
from app import app
from app.db.session import Session
from app.db.models import Club, ClubSchema, Event, User, Comment

from flask import Blueprint, abort, jsonify, request

from app.routes import user
from app.routes.authorize import login_required

@app.route('/b/clubs', methods=['GET'])
def get_all_clubs():
    clubs = Session().query(Club).all()
    schema = ClubSchema()
    return schema.dump(clubs, many=True)

@app.route('/b/clubs/<int:club_id>', methods=['GET'])
def get_club(club_id):
    session = Session()
    schema = ClubSchema()
    club = session.query(Club).get(club_id)
    return schema.dump(club)

@app.route('/b/clubs/name/<string:club_name>', methods=['GET'])
def get_club_by_name(club_name):
    session = Session()
    schema = ClubSchema()
    # Query the club by name
    
    conditions = []
    for letter in club_name:
        conditions.append(Club.name.ilike(f"%{letter}%"))
    
    clubs = session.query(Club).filter(and_(*conditions)).all()
    #clubs = session.query(Club).filter(Club.name.ilike(f"%{club_name}%")).all() 
    
    if not clubs: # Check if the list is empty
        return jsonify({'error': 'Club not found'}), 404
        
    return schema.dump(clubs, many=True)

@app.route('/b/clubs/new', methods=['POST'])
def create_club():
    session = Session()
    schema = ClubSchema()
    data = request.get_json()
    new_club = schema.load(data, session=session)
    session.add(new_club)
    session.commit()
    return schema.dump(new_club)

@app.route('/b/clubs/<int:club_id>', methods=['DELETE'])
def delete_club(club_id):
    session = Session()
    schema = ClubSchema()
    club = session.query(Club).get(club_id)
    session.delete(club)
    session.commit()
    return schema.dump(club)

@app.route('/b/clubs/<int:club_id>', methods=['PUT'])
def update_club(club_id):
    session = Session()
    data = request.get_json()
    club = session.query(Club).get(club_id)

    if not club: # Handle club not found
        return jsonify({'error': 'Club not found'}), 404

    schema.load(data, session=session, instance=club)
    session.commit()
    return schema.dump(club)

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
