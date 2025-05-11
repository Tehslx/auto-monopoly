class StatusHealth:

    def __init__(self, data: dict):
        self.json = data
        self.total = DataHealth(None)
        self.sections = Sections(None)

    @property
    def StatusHealth(self):
        self.total = DataHealth(self.json.get("total", None))
        self.sections = Sections(self.json.get("sections", None))
        return self

    def __str__(self):
        return str(self.json)


class DataHealth:

    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.uptime = None
            self.delay = None
        else:
            self.json = data
            self.uptime = self.json.get("uptime", None)
            self.delay = self.json.get("delay", None)

    def __str__(self):
        return str(self.json)


class Sections:

    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.market = None
            self.gchat = None
            self.inventory = None
            self.wallet = None
            self.users = None
            self.friends = None
            self.data = None
            self.trades = None
            self.im = None
            self.games = None
            self.rooms = None
            self.seasonpass = None
        else:
            self.json = data
            self.market = DataHealth(self.json.get("market", None))
            self.gchat = DataHealth(self.json.get("gchat", None))
            self.inventory = DataHealth(self.json.get("inventory", None))
            self.wallet = DataHealth(self.json.get("wallet", None))
            self.users = DataHealth(self.json.get("users", None))
            self.friends = DataHealth(self.json.get("friends", None))
            self.data = DataHealth(self.json.get("data", None))
            self.trades = DataHealth(self.json.get("trades", None))
            self.im = DataHealth(self.json.get("im", None))
            self.games = DataHealth(self.json.get("games", None))
            self.rooms = DataHealth(self.json.get("rooms", None))
            self.seasonpass = DataHealth(self.json.get("seasonpass", None))

    def __str__(self):
        return str(self.json)