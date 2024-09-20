from models import Users, db

class UserRepositories:

    def get_user_clubs(self, username):
        user = Users.query.filter_by(username=username).first()
        return user.clubs

    def get_user_interests(self, username):
        user = Users.query.filter_by(username=username).first()
        return user.interests