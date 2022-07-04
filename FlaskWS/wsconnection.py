import json
import copy
from .models import User
from . import db

class InvalidJSON(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Invalid JSON format. Reason -> {self.message}'


class AuthenticationFailed(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Authentication failed. Reason -> {self.message}'


class wsconnection:
    def __init__(self) -> None:
        self.connections = {}

    def formatdata(self, rawdata):
        try:
            data = json.loads(rawdata)
        except Exception as e:
            raise InvalidJSON('%s' % (e))
        
        return data

    def authenticate(self, data) -> bool:
        token = data['token']
        user = User.query.filter_by(sessionId=token).first()

        if not user:
            raise AuthenticationFailed('Invalid authentication token.')

        return True
        

