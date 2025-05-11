from .users_get import UsersGet
from .counters import Counters

class Auth:

    def __init__(self, data: dict):
        self.json = data
        self.status = None
        self.user_data = None
        self.counters = None

    @property
    def Auth(self):
        self.status = self.json.get("status", None)
        self.user_data = UsersGet(self.json.get("user_data", {})).UserData
        self.counters = Counters(self.json.get("counters", {})).Counters
        return self

    def __str__(self):
        return str(self.json)