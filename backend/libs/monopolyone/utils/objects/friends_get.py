class FriendsGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.count = None
        self.friends = None

    @property
    def FriendsGet(self):
        self.count = self.json.get("count", None)
        self.friends = self.json.get("friends", None)

        for index, friend in enumerate(map(Friends, self.friends), start=1):
            setattr(self, f"friend_{index}", friend)
            if index == 1: 
                self.friend_1 = friend 
            elif index == 2: 
                self.friend_2 = friend 
            elif index == 3: 
                self.friend_3 = friend 
            elif index == 4: 
                self.friend_4 = friend 
            elif index == 5: 
                self.friend_5 = friend 
        
        return self

    def __getattr__(self, data):
        if data.startswith("friend_"):
            return Friends(None)
    
    def __str__(self):
        return str(self.json)


class Friends:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.nickname = None
            self.nicks_old = None
            self.gender = None
            self.avatar_key = None
            self.avatar = None
            self.rank = None
            self.games = None
            self.games_wins = None
            self.xp = None
            self.xp_level = None
            self.friendship = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.nickname = self.json.get("nick", None)
            self.nicks_old = self.json.get("nicks_old", None)
            self.gender = self.json.get("gender", None)
            self.avatar_key = self.json.get("avatar_key", None)
            self.avatar = self.json.get("avatar", None)
            self.rank = self.json.get("rank", None)
            self.games = self.json.get("games", None)
            self.games_wins = self.json.get("games_wins", None)
            self.xp = self.json.get("xp", None)
            self.xp_level = self.json.get("xp_level", None)
            self.friendship = self.json.get("friendship", None)

    def __str__(self):
        return str(self.json)