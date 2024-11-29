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

If you want to set up your own database, follow the steps outlined at
https://wiki.archlinux.org/title/PostgreSQL, and set the `DATABASE_URL` to the
URL for the database you have created. Note that there is no need to create
tables, as the ORM will do this for you.

### Starting the Backend

To start the app:

    cd backend
    flask run

### Starting the Frontend

The frontend can be run with this command:

    npm start

The frontend includes a proxy to the backend, so while you are running this on
your local device, both the frontend and the backend can be accessed from the
same URL (by default with npm, `localhost:3000`).
