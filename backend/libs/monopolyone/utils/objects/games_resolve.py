class GamesResolve:

    def __init__(self, data: dict):
        self.json = data
        self.gs_id = None
        self.gs_game_id = None
        self.gs_token = None

    @property
    def GamesResolve(self):
        self.gs_id = self.json.get("gs_id", None)
        self.gs_game_id = self.json.get("gs_game_id", None)
        self.gs_token = self.json.get("gs_token", None)
        return self

    def __str__(self):
        return str(self.json)