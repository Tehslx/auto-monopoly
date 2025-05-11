class HistoryGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.messages = None
        self.users_data = None
        self.id_last = None

    @property
    def HistoryGet(self):
        self.messages = self.json.get("messages", None)
        self.users_data = self.json.get("users_data", None)
        self.id_last = self.json.get("id_last", None)

        for index, message in enumerate(map(MessageHistory, self.messages), start=1):
            setattr(self, f"message_{index}", message)
            if index == 1: 
                self.message_1 = message 
            elif index == 2: 
                self.message_2 = message 
            elif index == 3: 
                self.message_3 = message 
            elif index == 4: 
                self.message_4 = message 
            elif index == 5: 
                self.message_5 = message

        for index, user_data in enumerate(map(UsersDataHistory, self.users_data), start=1):
            setattr(self, f"user_data_{index}", user_data)
            if index == 1: 
                self.user_data_1 = user_data 
            elif index == 2: 
                self.user_data_2 = user_data 
            elif index == 3: 
                self.user_data_3 = user_data 
            elif index == 4: 
                self.user_data_4 = user_data 
            elif index == 5: 
                self.user_data_5 = user_data
        
        return self

    def __getattr__(self, data):
        if data.startswith("message_"):
            return MessageHistory(None)
        if data.startswith("user_data_"):
            return UsersDataHistory(None)

    def __str__(self):
        return str(self.json)
    

class MessageHistory:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.msg_id = None
            self.user_id = None
            self.ts_created = None
            self.is_read = None
            self.type = None
            self.text = None
        else:
            self.json = data
            self.msg_id = self.json.get("msg_id", None)
            self.user_id = self.json.get("user_id", None)
            self.ts_created = self.json.get("ts_created", None)
            self.is_read = self.json.get("is_read", None)
            self.type = self.json.get("type", None)
            self.text = self.json.get("text", None)

    def __str__(self):
        return str(self.json)


class UsersDataHistory:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.nickname = None
            self.gender = None
            self.avatar_key = None
            self.avatar = None
            self.online = None
            self.rank = None
            self.muted = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.nickname = self.json.get("nick", None)
            self.gender = self.json.get("gender", None)
            self.avatar_key = self.json.get("avatar_key", None)
            self.avatar = self.json.get("avatar", None)
            self.online = self.json.get("online", None)
            self.rank = self.json.get("rank", None)
            self.muted = self.json.get("muted", None)

    def __str__(self):
        return str(self.json)