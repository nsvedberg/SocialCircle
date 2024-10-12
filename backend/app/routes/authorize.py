from app import app
from app.db.session import Session
from app.db.models import User

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
            token = request.headers["Authorization"]
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
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        else:
            return {
                "message": "Error fetching auth token, invalid email or password",
                "error": "Unauthorized"
            }, 404
    except Exception as e:
        return {
                "message": "Something went wrong",
                "error": str(e),
        }, 500


@app.route("/b/current-user")
@login_required
def current_user(user):
    """Returns the currently logged-in user."""
    return jsonify(user)


# A list of OAuth2 providers that we support for alternate log-in.
app.config['OAUTH2_PROVIDERS'] = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server
    'google': {
        'client_id': getenv('GOOGLE_CLIENT_ID'),
        'client_secret': getenv('GOOGLE_CLIENT_SECRET'),
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
        'url_auth': 'https://accounts.google.com/o/oauth2/auth',
        'url_token': 'https://accounts.google.com/o/oauth2/token',
    },

    # GitHub OAuth 2.0 documentation:
    # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    'github': {
        'client_id': getenv('GITHUB_CLIENT_ID'),
        'client_secret': getenv('GITHUB_CLIENT_SECRET'),
        'userinfo': {
            'url': 'https://api.github.com/user/emails',
            'email': lambda json: json[0]['email'],
        },
        'scopes': ['user:email'],
        'url_auth': 'https://github.com/login/oauth/authorize',
        'url_token': 'https://github.com/login/oauth/access_token',
    },
}


@app.route('/b/authorize/<provider>')
def oauth2_authorize(provider):
    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)

    if provider_data is None:
        abort(404)

    # Generate a state parameter.
    # state = secrets.token_urlsafe(16)
    state = ""

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['url_auth'] + '?' + urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': state,
    }))


@app.route('/b/authorize/<provider>/callback')
def oauth2_callback(provider):
    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # If there was an authentication error, flash the error message and exit.
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # Make sure that the state parameter matches the one we created in the
    # authorization request.

    # TODO ...

    # Make sure that the authorization code is present.
    if 'code' not in request.args:
        abort(401)

    # Exchange the authorization code for an access token.
    response = requests.post(provider_data['url_token'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # Use the access token to get the user's email address.
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    session = Session()

    # Find or create the user in the database.
    user = User.get_by_email(email)
    if user is None:
        user = User(email=email, first_name="", last_name="")
        session.add(user)
        session.commit()

    token = encode_token(user.id)

    # Log the user in.
    return redirect('/login?token=' + token)
