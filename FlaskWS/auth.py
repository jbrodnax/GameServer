from crypt import methods
from flask import Blueprint, render_template, make_response, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import User
from . import db
import uuid

auth = Blueprint('auth', __name__)

# Decorator ensures a valid session token exists in the request.
# Sets flask.g.user to the verified user for downstream consumption
# Returns 403:'success':False on failed auth
def auth_required(fn):
    @wraps(fn)
    def wrap(*args, **kwargs):
        token = request.form.get('token')
        if not token:
            return jsonify(success=False), 403
        
        user = User.query.filter_by(sessionId=token).first()
        if not user:
            return jsonify(success=False), 403
        g.user = user
        return fn(*args, **kwargs)
    return wrap


# Login and start session. Token is used for WS connection
# Return token and 'success':True/False
@auth.route('/login', methods=['POST'])
def login():
    resp_body = {
        'success':False,
        'token':None
    }

    # Get name and pass from request body
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        return resp_body
    
    # Query for the user so we can check creds
    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password, password):
        return resp_body
    
    # Creds checked out. Generate session id (uuid4), 
    # save it to the User db, and return it to the client
    resp_body['token'] = str(uuid.uuid4())
    resp_body['success'] = True
    user.sessionId = resp_body['token']
    db.session.commit()

    resp = make_response(jsonify(resp_body), 200)
    return resp


# Account creation route
# Return 'success':True/False
@auth.route('/signup', methods=['POST'])
def signup():
    resp_body = {
        'success':False
    }

    # Get name and pass from request body
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        return resp_body
    
    # Query name to see if it already exists
    user = User.query.filter_by(name=name).first()
    if user:
        return resp_body
    
    # Create a new user in the database.
    new_user = User(name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    resp_body['success']=True
    resp = make_response(jsonify(resp_body), 200)
    return resp


# Session logout
# Return 'success':True/False
@auth.route('/logout', methods=['POST'])
@auth_required
def logout():
    resp_body = {
        'success':False
    }

    # Remove the sessionId from that user's db entry
    user = g.user
    user.sessionId = None
    db.session.commit()

    resp_body['success'] = True

    resp = make_response(jsonify(resp_body), 200)
    return resp


# Testing interface for websocket API
@auth.route('/')
@auth_required
def index():
    return render_template('index.html')