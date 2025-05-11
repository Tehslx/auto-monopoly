from .users_get import UsersGet


class GamesMy:
    
    def __init__(self, data: dict):
        self.json = data
        self.count = None
        self.games = Games(None)
        self.users_data = UsersGet(None)

    @property
    def GamesMy(self):
        self.count = self.json.get("count", None)
        self.games = self.json.get("games", None)
        self.users_data = UsersGet(self.json.get("users_data", None)).UsersGet

        for index, game in enumerate(map(Games, self.games), start=1):
            setattr(self, f"game_{index}", game)
            if index == 1: 
                self.game_1 = game 
            elif index == 2: 
                self.game_2 = game 
            elif index == 3: 
                self.game_3 = game 
            elif index == 4: 
                self.game_4 = game 
            elif index == 5: 
                self.game_5 = game
        
        return self

    def __getattr__(self, data):
        if data.startswith("game_"):
            return Games(None)
    
    def __str__(self):
        return str(self.json)


class Games:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.game_id = None
            self.status = None
            self.gs_id = None
            self.gs_game_id = None
            self.game_mode = None
            self.game_submode = None
            self.game_2x2 = None
            self.players = None
            self.ts_start = None
            self.ts_end = None
        else:
            self.json = data
            self.game_id = self.json.get("game_id", None)
            self.status = self.json.get("status", None)
            self.gs_id = self.json.get("gs_id", None)
            self.gs_game_id = self.json.get("gs_game_id", None)
            self.game_mode = self.json.get("game_mode", None)
            self.game_submode = self.json.get("game_submode", None)
            self.game_2x2 = self.json.get("game_2x2", None)
            self.players = self.json.get("players", None)
            self.ts_start = self.json.get("ts_start", None)
            self.ts_end = self.json.get("ts_end", None)


            for index, player in enumerate(map(Players, self.players), start=1):
                setattr(self, f"player_{index}", player)
                if index == 1: 
                    self.player_1 = player 
                elif index == 2: 
                    self.player_2 = player 
                elif index == 3: 
                    self.player_3 = player 
                elif index == 4: 
                    self.player_4 = player 
                elif index == 5: 
                    self.player_5 = player

    def __getattr__(self, data):
        if data.startswith("player_"):
            return Players(None)    
    
    def __str__(self):
        return str(self.json)


class Players:

    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.xp = None
            self.points = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.xp = self.json.get("xp", None)
            self.points = self.json.get("points", None)

    def __str__(self):
        return str(self.json)