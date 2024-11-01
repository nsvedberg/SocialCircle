import os

from dotenv import load_dotenv
from flask import Flask

from app.db.session import init_db

from os import getenv

# If you get a build error and index.html is being served, it's because this is different, move your .env file
if not getenv("SCIRCLE_DEVELOP"):
    load_dotenv("/etc/socialcircle.conf")
app = Flask(__name__)

app.secret_key = getenv("FLASK_SECRET_KEY")

from app import routes

if getenv("SCIRCLE_DEVELOP"):
    from app.routes import develop

init_db()

if __name__ == "__main__":
    if getenv("SCIRCLE_DEVELOP"):
        app.run(debug=True)
    else:
        app.run()
