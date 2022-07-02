from flask import Blueprint
from . import sock

socka = Blueprint('sock', __name__)

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)

@socka.route('/echoa')
def echo(ws):
    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)
