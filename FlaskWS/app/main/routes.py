from flask import render_template, request
from . import main


@main.route('/', methods=['GET'])
def index():
    """Login form to enter a room."""
    return render_template('index.html')
