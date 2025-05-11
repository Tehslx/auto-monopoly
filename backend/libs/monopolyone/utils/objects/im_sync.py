class ImSync:

    def __init__(self, data: dict):
        self.json = data
        self.id = None
        self.type = None
        self.id_last = None

    @property
    def ImSync(self):
        self.id = self.json.get("id", None)
        self.type = self.json.get("type", None)
        self.id_last = self.json.get("id_last", None)
        return self

    def __str__(self):
        return str(self.json)