class CurrentGame:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.gs_id = None
            self.gs_game_id = None
        else:
            self.json = data
            self.gs_id = self.json.get("gs_id", None)
            self.gs_game_id = self.json.get("gs_game_id", None)

    def __str__(self):
        return str(self.json)