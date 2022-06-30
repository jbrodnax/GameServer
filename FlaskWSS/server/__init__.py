from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Init SQLAlchemy
db = SQLAlchemy()
socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)

    # TKTK - move key to config file
    app.config['SECRET_KEY'] = 'quackenKraken'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.debug = debug
    
    db.init_app(app)

    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)

    return app