from .status import Status
from .auth import Auth
from .events import Events

class Event:

    def __init__(self, data: dict):
        self.json = data
        self.type = None
        self.data = None

    @property
    def Event(self):
        self.type = self.json.get("type", None)
        if self.type == "status":
            self.data = Status(self.json.get("status", {})).Status
        elif self.type == "auth":
            self.data = Auth(self.json).Auth
        elif self.type == "events":
            self.data = Events(self.json).Events
        return self