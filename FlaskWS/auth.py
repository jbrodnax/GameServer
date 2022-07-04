from crypt import methods
from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
import uuid

auth = Blueprint('auth', __name__)


# Login and start session. Token is used for WS connection
# Return token and 'success':True/False
@auth.route('/login', methods=['POST'])
def login():
    resp = {
        'success':False,
        'token':None
    }

    # Get name and pass from request body
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        return resp
    
    # Query for the user so we can check creds
    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password, password):
        return resp
    
    # Creds checked out. Generate session id (uuid4), 
    # save it to the User db, and return it to the client
    resp['token'] = str(uuid.uuid4())
    user.sessionId = resp['token']
    db.session.commit()

    return resp


# Account creation route
# Return 'success':True/False
@auth.route('/signup', methods=['POST'])
def signup():
    resp = {
        'success':False
    }

    # Get name and pass from request body
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        return resp
    
    # Query name to see if it already exists
    user = User.query.filter_by(name=name).first()
    if user:
        return resp
    
    # Create a new user in the database.
    new_user = User(name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    resp['success']=True
    return resp


# Session logout
# Return 'success':True/False
@auth.route('/logout', methods=['POST'])
def logout():
    resp = {
        'success':False
    }

    # Get the sessionID from the request body
    token = request.form.get('token')

    if not token:
        return resp
    
    # Query for user that has the supplied session id
    user = User.query.filter_by(sessionId=token).first()
    if not user:
        return resp

    # Remove the sessionId from that user's db entry
    user.sessionId = None
    db.session.commit()

    resp['success'] = True

    return resp

@auth.route('/')
def index():
    return render_template('index.html')