from flask import Blueprint
from . import sock

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)
