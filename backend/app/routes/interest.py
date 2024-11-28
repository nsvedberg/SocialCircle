from app import app
from app.db.session import Session
from app.db.models import Club, Interest, InterestSchema

from flask import request

from app.routes.authorize import login_required

@app.route('/b/interests', methods=['GET'])
def get_all_interests():
    interests = Session().query(Interest).all()
    schema = InterestSchema()
    return schema.dump(interests, many=True)

@app.route('/b/interests/<int:interest_id>', methods=['GET'])
def get_interest(interest_id):
    interest = Session().query(Interest).get(interest_id)
    schema = InterestSchema()
    return schema.dump(interest)

@login_required
@app.route('/b/interests/new', methods=['POST'])
def create_interest():
    session = Session()
    schema = InterestSchema()
    data = request.get_json()
    new_interest = schema.load(data, session=session)
    session.add(new_interest)
    session.commit()
    return schema.dump(new_interest)

@login_required
@app.route('/b/interests/<int:interest_id>', methods=['PUT'])
def update_interest(interest_id):
    session = Session()
    schema = InterestSchema()
    data = request.get_json()
    interest = session.query(Interest).get(interest_id)
    schema.load(data, session=session, instance=interest)
    session.commit()
    return schema.dump(interest)

@login_required
@app.route('/b/interests/<int:interest_id>', methods=['DELETE'])
def delete_interest(interest_id):
    session = Session()
    schema = InterestSchema()
    interest = session.query(Interest).get(interest_id)
    session.delete(interest)
    session.commit()
    return schema.dump(interest)
