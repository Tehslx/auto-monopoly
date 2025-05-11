class GlobalChatAdd:

    def __init__(self, data: dict):
        self.json = data
        self.id = None
        self.msg_id = None
        self.type = None

    @property
    def GlobalChatAdd(self):
        self.id = self.json.get("id", None)
        self.msg_id = self.json.get("msg_id", None)
        self.type = self.json.get("type", None)
        return self

    def __str__(self):
        return str(self.json)