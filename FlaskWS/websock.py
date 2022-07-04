from flask import Blueprint
from flask_sock import Sock
from . import myapp
from .wsconnection import wsconnection

sock = Sock()

@sock.route('/echo')
def echo(ws):
    wsconn = wsconnection()
    rawdata = ws.receive()

    try:
        data = wsconn.formatdata(rawdata)
    except Exception as e:
        myapp.logger.info('Exception: %s', e)
        return
    
    try:
        wsconn.authenticate(data)
    except Exception as e:
        myapp.logger.info('Exception: %s', e)
        return
    
    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)
