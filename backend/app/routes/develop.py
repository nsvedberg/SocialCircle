from app import app
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('../../frontend/build/', 'index.html')

@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('../../frontend/build/', path)
