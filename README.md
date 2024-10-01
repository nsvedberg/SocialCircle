# SocialCircle

![logo](logo.png)

SocialCircle is a modern social media app designed to drive student engagement
on campus.

## Usage

This app uses ReactJS for the frontend and Flask/Python on the backend. In
order to get the app running, there are a couple of setup steps.

### Environment

The app requires a few secrets and credentials to be run. There is a file named
`.env` in the discord channel called `#env`. Download this file into the
backend directory, where you will be running Flask from.


    DATABASE_URL="..."
    SCIRCLE_DEVELOP="true"
    GOOGLE_CLIENT_ID="..."
    GOOGLE_CLIENT_SECRET="..."
    GITHUB_CLIENT_ID="..."
    GITHUB_CLIENT_SECRET="..."
    FLASK_SECRET_KEY="..."

### Database

The database is already running at `socialcircle.muuu.net`. The provided
environment file contains a URL to the database which includes your access
credentials.

In the future, I think it will make sense to create an additional database for
production. For now, there is only one database.

### Building the Frontend

The frontend can be build with this command:

    cd frontend
    npm run build

Then, all of the built files will be in the `build/` directory.

By the way, while developing the frontend, you can also host it on its own
like this:

    npm start

### Starting the Backend

To start the app:

    cd backend
    flask run

By default, when running in develop mode (see the above `SCIRCLE_DEVELOP`
environment parameter), Flask will host the built files from the frontend
statically (using a relative path). This will only work if you have already
built the frontend and will not update with changes you make until you re-build
the frontend.
