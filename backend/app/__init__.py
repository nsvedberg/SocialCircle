import os

from flask import Flask
from flask_cors import CORS

from app.db.session import init_db

from os import getenv

if getenv("SCIRCLE_DEVELOP"):
    app = Flask(__name__,
                static_url_path=None,
                static_folder="../../frontend/build")
else:
    app = Flask(__name__)

CORS(app, resources={r"/clubs/*": {"origins": "http://localhost:3000"}})

app.secret_key = getenv("FLASK_SECRET_KEY")

from app import routes

if getenv("SCIRCLE_DEVELOP"):
    from app.routes import develop

init_db()

if __name__ == "__main__":
    if getenv("SCIRCLE_DEVELOP"):
        app.run()
    else:
        app.run(debug=True)
