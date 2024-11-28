import os

from dotenv import load_dotenv
from flask import Flask

from app.db.session import init_db

from os import getenv

#if not getenv("SCIRCLE_DEVELOP"):
 #   load_dotenv("/etc/socialcircle.conf")
#app = Flask(__name__)

# I get a build error with the above code, even after relocating the env, so I
# am going to keep using this for now
if getenv("SCIRCLE_DEVELOP"):
    app = Flask(__name__,
                static_url_path=None,
                static_folder="../../frontend/build")
else:
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
