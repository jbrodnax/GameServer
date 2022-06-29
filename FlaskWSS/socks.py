from flask_sock import Sock
from . import app

sock = Sock(app)

@sock.route('/wshandler')
def wshandler(ws):
    while True:
        data = ws.receive()
        ret = 'echo: '+data
        ws.send(ret)