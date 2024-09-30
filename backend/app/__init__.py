from flask import Flask

from app.db.session import init_db

app = Flask(__name__)

from app import routes

init_db()

if __name__ == "__main__":
    app.run(debug=True)
