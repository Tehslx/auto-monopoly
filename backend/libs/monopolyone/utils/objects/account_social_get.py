from .users_get import UsersGet


class AccountSocialGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.vk = VK(None)
        self.discord = DISCORD(None)
        self.twitch = TWITCH(None)

    @property
    def AccountSocialGet(self):
        self.vk = VK(self.json.get("vk", None))
        self.discord = DISCORD(self.json.get("discord", None))
        self.twitch = TWITCH(self.json.get("twitch", None))
        
        return self
    
    def __str__(self):
        return str(self.json)


class VK:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.id = None
            self.screen_name = None
            self.avatar = None
            self.last_name = None
            self.first_name = None
        else:
            self.json = data
            self.id = self.json.get("id", None)
            self.screen_name = self.json.get("screen_name", None)
            self.avatar = self.json.get("avatar", None)
            self.last_name = self.json.get("last_name", None)
            self.first_name = self.json.get("first_name", None)

    def __str__(self):
        return str(self.json)


class DISCORD:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.id = None
            self.discriminator = None
            self.username = None
            self.avatar = None
        else:
            self.json = data
            self.id = self.json.get("id", None)
            self.discriminator = self.json.get("discriminator", None)
            self.username = self.json.get("username", None)
            self.avatar = self.json.get("avatar", None)

    def __str__(self):
        return str(self.json)


class TWITCH:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.id = None
            self.display_name = None
            self.avatar = None
        else:
            self.json = data
            self.id = self.json.get("id", None)
            self.display_name = self.json.get("display_name", None)
            self.avatar = self.json.get("avatar", None)

    def __str__(self):
        return str(self.json)