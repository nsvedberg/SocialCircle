import os
from flask import Flask
from db.session import init_db
from os import getenv

def create_app():
    # Set up the Flask app
    app = Flask(__name__)

    if getenv("SCIRCLE_DEVELOP"):
        # Serve frontend static files when in development mode
        app.static_url_path = None
        app.static_folder = "../../frontend/build"
    
    app.secret_key = getenv("FLASK_SECRET_KEY")

    # Import router inside the function to avoid circular imports
    from routes.routes import router
    app.register_blueprint(router)  # Register the Blueprint

    # Initialize the database
    init_db()

    return app

# Main entry point
if __name__ == "__main__":
    # Create the Flask app
    app = create_app()

    # Run the app
    if getenv("SCIRCLE_DEVELOP"):
        app.run(debug=True)
    else:
        app.run()
