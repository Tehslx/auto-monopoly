class UsersData:

    def __init__(self, data: dict):
        self.json = data
        self.avatar = None
        self.gender = None
        self.nick = None
        self.online = None
        self.rank = {}
        self.user_id = None
        self.vip = None

    @property
    def UsersData(self):
        self.avatar = self.json.get("avatar", None)
        self.gender = self.json.get("gender", None)
        self.nick = self.json.get("nick", None)
        self.online = self.json.get("online", None)
        self.rank = self.json.get("rank", {})
        self.user_id = self.json.get("user_id", None)
        self.vip = self.json.get("vip", None)
        return self

    def __str__(self):
        return str(self.json)