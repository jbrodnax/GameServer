from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sock import Sock

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
sock = Sock()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
    app.debug = True

    db.init_app(app)
    sock.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    #from .sock import socka as socka_blueprint
    #app.register_blueprint(socka_blueprint)

    return app