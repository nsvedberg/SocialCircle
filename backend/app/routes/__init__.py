from operator import and_
from app import app
from app.db.session import Session
from app.db.models import Club, Event, User, Comment

from flask import Blueprint, abort, jsonify, request

from app.routes.authorize import login_required

import app.routes.authorize
import app.routes.user
import app.routes.club
import app.routes.event
