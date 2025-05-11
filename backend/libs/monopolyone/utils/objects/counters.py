class Counters:

    def __init__(self, data: dict):
        self.json = data
        self.vip_expires = None
        self.balance = None
        self.friends_requests = None
        self.messages_new = None
        self.invites = None
        self.trades_new = None
        self.email_verified = None

    @property
    def Counters(self):
        self.vip_expires = self.json.get("vip_expires", None)
        self.balance = self.json.get("balance", None)
        self.friends_requests = self.json.get("friends_requests", None)
        self.messages_new = self.json.get("messages_new", None)
        self.invites = self.json.get("invites", None)
        self.trades_new = self.json.get("trades_new", None)
        self.email_verified = self.json.get("email_verified", None)
        return self

    def __str__(self):
        return str(self.json)