from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sock import Sock

# Init SQLAlchemy
db = SQLAlchemy()
#sock = Sock()

def create_app():
    app = Flask(__name__)

    # TKTK - move key to config file
    app.config['SECRET_KEY'] = 'quackenKraken'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    #sock.init_app(app)

    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app