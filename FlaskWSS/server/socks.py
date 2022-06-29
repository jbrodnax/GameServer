from . import sock

@sock.route('/wshandler')
def wshandler(ws):
    while True:
        data = ws.receive()
        ret = 'echo: '+data
        ws.send(ret)