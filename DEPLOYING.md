These are steps for deploying the application to a server. The server I'm using
is running Debian 12 (bookworm).

We will need the following packages:

- nginx
- npm
- postgres
- uwsgi
- uwsgi-plugin-python3

On this server, the user/group www-data already exists. If it didn't exist, you
could create it like this:

    # useradd -r www-data

We will also create the user www-socialcircle:

    # useradd -r www-socialcircle

We will create a place to put the application:

    # install -d -m 0770 -o www-socialcircle -g www-data /srv/socialcircle

And a place to put uWSGI's socket file:

    # install -d -m 0770 -o www-socialcircle -g www-data /var/run/socialcircle

And a place to put the environment file:

    # install -d -m 0700 -o www-socialcircle -g www-socialcircle /etc/socialcircle

The environment file is not contained into the repo because it contains
secrets. You can upload this file using SFTP, into the above directory.

We'll get the repository files from git:

    $ cd /srv/socialcircle
    $ git clone https://github.com/nsvedberg/SocialCircle.git .

Build the frontend:

    $ cd /srv/socialcircle/frontend
    $ npm install
    $ npm run build

And install the configuration files:

    # install -m 644 -o www-data -g www-data /srv/socialcircle/dist/nginx.conf \
        /etc/nginx/sites-available/socialcircle.muuu.net
    # ln -s /etc/nginx/sites-available/socialcircle.muuu.net \
        /etc/nginx/sites-enabled/
    # install -m 644 -o root -g root /srv/socialcircle/dist/systemd.service \
        /etc/systemd/system/socialcircle.service
    # install -m 644 -o root -g root /srv/socialcircle/dist/uwsgi.ini \
        /etc/uwsgi/apps-available/socialcircle.ini
    # ln -s /etc/uwsgi/apps-available/socialcircle.ini \
        /etc/uwsgi/apps-enabled/

After this, the service can be started like this:

    # systemctl daemon-reload
    # systemctl start socialcircle

And enabled to run on reboot:

    # systemctl enable socialcircle
