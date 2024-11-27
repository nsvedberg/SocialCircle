from app import app
from flask import send_from_directory, redirect, url_for

@app.route('/')
def react_index():
    return send_from_directory('../../frontend/build/', 'index.html')

@app.route('/<path:path>')
def react_catch_all(path):
    return send_from_directory('../frontend/build/', path)

@app.errorhandler(404)
def react_not_found(e):
    return send_from_directory('../../frontend/build/', 'index.html')
