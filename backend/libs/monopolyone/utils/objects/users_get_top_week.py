from .users_get import UsersGet


class UsersGetTopWeek:

    def __init__(self, data: dict):
        self.json = data
        self.prize_pool = None
        self.top = None
        self.users_data = UsersGet(None)

    @property
    def UsersGetTopWeek(self):
        self.prize_pool = self.json.get("prize_pool", None)
        self.top = self.json.get("top", None)
        self.users_data = UsersGet(self.json.get("users_data", None)).UsersGet

        for index, topweek in enumerate(map(Top, self.top), start=1):
            setattr(self, f"top_{index}", topweek)
            if index == 1: 
                self.top_1 = topweek 
            elif index == 2: 
                self.top_2 = topweek 
            elif index == 3: 
                self.top_3 = topweek 
            elif index == 4: 
                self.top_4 = topweek 
            elif index == 5: 
                self.top_5 = topweek
        
        return self

    def __getattr__(self, data):
        if data.startswith("top_"):
            return Top(None)

    def __str__(self):
        return str(self.json)


class Top:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.position = None
            self.user_id = None
            self.score = None
        else:
            self.json = data
            self.position = self.json.get("position", None)
            self.user_id = self.json.get("user_id", None)
            self.score = self.json.get("score", None)

    def __str__(self):
        return str(self.json)