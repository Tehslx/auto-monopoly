from .users_get import UsersGet


class BlacklistGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.count = None
        self.users = UsersGet(None)

    @property
    def BlacklistGet(self):
        self.count = self.json.get("count", None)
        self.users = UsersGet(self.json.get("users", None)).UsersGet
        
        return self
    
    def __str__(self):
        return str(self.json)