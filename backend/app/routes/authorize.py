from app import app
from app.db.session import Session
from app.db.models import User, UserSchema

from flask import current_app, jsonify
from flask import request, abort, redirect, url_for
from functools import wraps

from urllib.parse import urlencode
from sqlalchemy import select

import jwt
from os import getenv

import datetime
import requests

def encode_token(user_id):
    # token should expire after 24 hrs
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    return jwt.encode(
        {"user_id": user_id, "exp": expiration_time},
        app.secret_key,
        algorithm="HS256"
    )

def decode_token(token):
    data=jwt.decode(token, app.secret_key, algorithms=["HS256"],
                    options={"require": ["exp"]})

    return data["user_id"]

def login_required(f):
    """
    Decorator to indicated that a route requires a token to access.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        session = Session()

        # Get the token from the Authorization header.
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].removeprefix("Bearer ")
        if not token:
            return {
                "message": "Authentication Token is missing.",
                "error": "Unauthorized"
            }, 401
        try:
            # Decode the token.
            user_id = decode_token(token)

            # Get the user specified in the token.
            current_user=session.get(User, user_id)

            if current_user is None:
                return {
                "message": "Invalid Authentication token.",
                "error": "Unauthorized"
            }, 401

            if not current_user.is_active:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong.",
                "error": str(e)
            }, 500

        # Carry out the view, using the current user.
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/b/login", methods=["POST"])
def login():
    """
    Log in with a username and password. If the login request is successful,
    return an authorization token.
    """
    session = Session()

    try:
        data = request.json

        if not data:
            return {
                "message": "Invalid user data.",
                "error": "Bad request"
            }, 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {
                "message": "Invalid user data.",
                "error": "Bad request"
            }, 400

        user = User.get_by_email(data["email"])

        if user and user.check_password(password):
            try:
                token = encode_token(user.id)
                return {
                    "message": "Successfully fetched auth token",
                    "data": token
                }
            except Exception as e:
                return {
                    "message": str(e),
                    "error": "Something went wrong",
                }, 500
        else:
            return {
                "message": "Error fetching auth token, invalid email or password",
                "error": "Unauthorized"
            }, 404
    except Exception as e:
        return {
                "message": str(e),
                "error": "Something went wrong",
        }, 500


@app.route("/b/current-user")
@login_required
def current_user(user):
    """Returns the currently logged-in user."""
    return UserSchema().dump(user)

app.config['oauth2'] = {
    'github': {
        'permissions': ['user:email'],
        'url_auth': 'https://github.com/login/oauth/authorize',
        'cl_scrt': getenv('GITHUB_CLIENT_SECRET'),
        'cid': getenv('GITHUB_CLIENT_ID'),
        'info': {
            'url': 'https://api.github.com/user/emails',
            'email': lambda json: json[0]['email'],
        },
        'url_token': 'https://github.com/login/oauth/access_token',
    },

    'google': {
        'cl_scrt': getenv('GOOGLE_CLIENT_SECRET'),
        'cid': getenv('GOOGLE_CLIENT_ID'),
        'url_auth': 'https://accounts.google.com/o/oauth2/auth',
        'permissions': ['https://www.googleapis.com/auth/userinfo.email'],
        'url_token': 'https://accounts.google.com/o/oauth2/token',
        'info': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
    },
}

@app.route('/b/authorize/<provider>/callback')
def oauth2_callback(provider):
    prov = current_app.config['oauth2'].get(provider)

    res = requests.post(prov['url_token'], data={
        'code': request.args['code'],
        'client_secret': prov['cl_scrt'],
        'grant_type': 'authorization_code',
        'client_id': prov['cid'],
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})

    tok = res.json().get('access_token')

    res = requests.get(prov['info']['url'], headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tok,
    })

    email = prov['info']['email'](res.json())

    session = Session()

    user = User.get_by_email(email)
    if user is None:
        user = User(email=email, first_name="", last_name="")
        session.add(user)
        session.commit()

    token = encode_token(user.id)

    return redirect('/login?token=' + token)

@app.route('/b/authorize/<provider>')
def oauth2_authorize(provider):
    prov = current_app.config['oauth2'].get(provider)

    return redirect(prov['url_auth'] + '?' + urlencode({
        'state': '',
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
        'client_id': prov['cid'],
        'scope': ' '.join(prov['permissions']),
        'response_type': 'code',
    }))
