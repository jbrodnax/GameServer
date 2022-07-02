from flask import session, redirect, url_for, render_template, request
from . import main


@main.route('/', methods=['GET'])
def index():
    """Login form to enter a room."""
    session['name'] = "testname"
    session['room'] = "testroom"
    return redirect(url_for('.chat'))

@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    return render_template('chat.html', name=name, room=room)