import json
from .models import User
from . import db

class wsconnection:
    def __init__(self) -> None:
        self.connections = {}

    def formatdata(self, rawdata):
        try:
            data = json.loads(rawdata)
        except Exception as e:
            print('ws request contain invalid data: '+e)
            return None
        
        return data

    def authenticate(self, data) -> bool:
        token = data['token']
        user = User.query.filter_by(sessionId=token).first()
        if not user:
            return False
        return True
        

