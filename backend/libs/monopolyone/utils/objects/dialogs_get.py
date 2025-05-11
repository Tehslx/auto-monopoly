class DialogsGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.dialogs = None
        self.users_data = None
        self.id_last = None

    @property
    def DialogsGet(self):
        self.dialogs = self.json.get("dialogs", None)
        self.users_data = self.json.get("users_data", None)
        self.id_last = self.json.get("id_last", None)

        for index, dialog in enumerate(map(Dialogs, self.dialogs), start=1):
            setattr(self, f"dialog_{index}", dialog)
            if index == 1: 
                self.dialog_1 = dialog 
            elif index == 2: 
                self.dialog_2 = dialog 
            elif index == 3: 
                self.dialog_3 = dialog 
            elif index == 4: 
                self.dialog_4 = dialog 
            elif index == 5: 
                self.dialog_5 = dialog
        
        for index, user_data in enumerate(map(UsersDataDialogs, self.users_data), start=1):
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
        if data.startswith("dialog_"):
            return Dialogs(None)
        if data.startswith("user_data_"):
            return UsersDataDialogs(None)

    def __str__(self):
        return str(self.json)


class Dialogs:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.new_counter = None
            self.message = MessageDialogs(None)
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.new_counter = self.json.get("new_counter", None)
            self.message = MessageDialogs(self.json.get("message", None))
    
    def __str__(self):
        return str(self.json)


class MessageDialogs:
    
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


class UsersDataDialogs:
    
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