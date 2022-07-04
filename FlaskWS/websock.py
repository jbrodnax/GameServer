from flask import Blueprint
from flask_sock import Sock
from . import wsconnection

sock = Sock()

@sock.route('/echo')
def echo(ws):
    wsconn = wsconnection()
    rawdata = ws.receive()
    data = wsconn.formatdata(rawdata)
    if not data:
        return
    if wsconn.authenticate(data) is False:
        return

    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)
