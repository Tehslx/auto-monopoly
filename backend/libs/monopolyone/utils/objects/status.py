class Status:

    def __init__(self, data: dict):
        self.json = data
        self.time = None
        self.online = None
        self.streams = None
        self.sct = None
        self.emotes_restricted = None

    @property
    def Status(self):
        self.time = self.json.get("time", None)
        self.online = self.json.get("online", None)
        self.streams = self.json.get("streams", None)
        self.sct = self.json.get("sct", None)
        self.emotes_restricted = self.json.get("emotes_restricted", None)
        return self

    def __str__(self):
        return str(self.json)