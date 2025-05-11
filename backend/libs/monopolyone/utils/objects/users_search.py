class UsersSearch:
    
    def __init__(self, data: dict):
        self.json = data
        self.count = None
        self.users_result = UserResult(None)

    @property
    def UsersSearch(self):
        self.count = self.json.get("count", None)
        self.users_result = self.json.get("result", None)

        for index, user_result in enumerate(map(UserResult, self.users_result), start=1):
            setattr(self, f"user_{index}", user_result)
            if index == 1: 
                self.user_1 = user_result 
            elif index == 2: 
                self.user_2 = user_result 
            elif index == 3: 
                self.user_3 = user_result 
            elif index == 4: 
                self.user_4 = user_result 
            elif index == 5: 
                self.user_5 = user_result
        
        return self

    def __getattr__(self, data):
        if data.startswith("user_"):
            return UserResult(None)
    
    def __str__(self):
        return str(self.json)


class UserResult:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.nickname = None
            self.gender = None
            self.avatar_key = None
            self.avatar = None
            self.rank = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.nickname = self.json.get("nick", None)
            self.gender = self.json.get("gender", None)
            self.avatar_key = self.json.get("avatar_key", None)
            self.avatar = self.json.get("avatar", None)
            self.rank = self.json.get("rank", None)  
    
    def __str__(self):
        return str(self.json)