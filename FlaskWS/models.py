from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # primary keys are required by SQLAlchemy
    sessionId = db.Column(db.String(100), unique=True)   # Session uuid associated with WS connection
    gameId = db.Column(db.String(100), unique=True)     # uuid of the user's current game
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)  # Name of the game as defined by creator
    state = db.Column(db.String(100))               # String representation of the game's state