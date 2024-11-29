from app import app
from app.db.session import Session
from app.db.models import Club, User, UserSchema

from flask import request

from app.routes.authorize import login_required

@app.route('/b/users', methods=['GET'])
def get_all_users():
    users = Session().query(User).all()
    schema = UserSchema()
    return schema.dump(users, many=True)

@app.route('/b/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Session().query(User).get(user_id)
    schema = UserSchema()
    return schema.dump(user)

@login_required
@app.route('/b/users/new', methods=['POST'])
def create_user():
    session = Session()
    schema = UserSchema()
    data = request.get_json()
    new_user = schema.load(data, session=session)
    session.add(new_user)
    session.commit()
    return schema.dump(new_user)

@login_required
@app.route('/b/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = Session()
    schema = UserSchema()
    data = request.get_json()
    print(data)
    user = session.query(User).get(user_id)
    schema.load(data, session=session, instance=user)
    session.commit()
    return schema.dump(user)

@login_required
@app.route('/b/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    schema = UserSchema()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return schema.dump(user)

# maybe not needed?
@login_required
@app.route('/b/users/<int:user_id>/add-to-club/<int:club_id>', methods=['POST'])
def add_user_to_club(user_id, club_id):
    session = Session()
    schema = UserSchema()
    user = session.query(User).get(user_id)
    club = session.query(Club).get(club_id)
    user.clubs.append(club)
    session.commit()
    return schema.dump(user)
