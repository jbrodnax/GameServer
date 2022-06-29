from . import socketio

@socketio.on('text', namespace='/wshandler')
def wshandler(ws):
    while True:
        data = ws.receive()
        ret = 'echo: '+data
        ws.send(ret)