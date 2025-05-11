class ProfileGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.user = None
        self.friends = None
        self.inventory = None
        self.note = None
        self.posts = None

    @property
    def ProfileGet(self):
        self.user = UserProfile(self.json.get("user", None))
        self.friends = FriendsProfile(self.json.get("friends", None))
        self.inventory = InventoryProfile(self.json.get("inventory", None))
        self.note = NoteProfile(self.json.get("note", None))
        self.posts = PostsProfile(self.json.get("posts", None))
        return self

    def __str__(self):
        return str(self.json)

class UserProfile:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.nickname = None
            self.nicks_old = None
            self.gender = None
            self.avatar_key = None
            self.avatar = None
            self.online = None
            self.rank = None
            self.games = None
            self.games_wins = None
            self.xp = None
            self.xp_level = None
            self.admin_rights = None
            self.penalties = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.nickname = self.json.get("nick", None)
            self.nicks_old = self.json.get("nicks_old", None)
            self.gender = self.json.get("gender", None)
            self.avatar_key = self.json.get("avatar_key", None)
            self.avatar = self.json.get("avatar", None)
            self.online = self.json.get("online", None)
            self.rank = self.json.get("rank", None)
            self.games = self.json.get("games", None)
            self.games_wins = self.json.get("games_wins", None)
            self.xp = self.json.get("xp", None)
            self.xp_level = self.json.get("xp_level", None)
            self.admin_rights = self.json.get("admin_rights", None)
            self.penalties = self.json.get("penalties", None)
            
    def __str__(self):
        return str(self.json)


class FriendsProfile:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.count = None
            self.friends = None
        else:
            self.json = data
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


class InventoryProfile:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.count = None
            self.things = None
            self.collections = None
            self.thing_types = None
            self.qualities = None
        else:
            self.json = data
            self.count = self.json.get("count", None)
            self.things = self.json.get("things", None)
            self.collections = self.json.get("collections", None)
            self.thing_types = self.json.get("thing_types", None)
            self.qualities = self.json.get("qualities", None)
            
    def __str__(self):
        return str(self.json)


class NoteProfile:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.user_id_about = None
            self.text = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.user_id_about = self.json.get("user_id_about", None)
            self.text = self.json.get("text", None)
            
    def __str__(self):
        return str(self.json)


class PostsProfile:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.count = None
            self.posts = None
            self.users = None
        else:
            self.json = data
            self.count = self.json.get("count", None)
            self.posts = self.json.get("posts", None)
            self.users = self.json.get("users", None)
            
        for index, user in enumerate(map(Users, self.users), start=1):
            setattr(self, f"user_{index}", user)
            if index == 1: 
                self.user_1 = user 
            elif index == 2: 
                self.user_2 = user 
            elif index == 3: 
                self.user_3 = user 
            elif index == 4: 
                self.user_4 = user 
            elif index == 5: 
                self.user_5 = user 

    def __getattr__(self, data):
        if data.startswith("user_"):
            return Users(None)

    def __str__(self):
        return str(self.json)


class Users:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.nickname = None
            self.gender = None
            self.avatar_key = None
            self.avatar = None
            self.online = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.nickname = self.json.get("nick", None)
            self.gender = self.json.get("gender", None)
            self.avatar_key = self.json.get("avatar_key", None)
            self.avatar = self.json.get("avatar", None)
            self.online = self.json.get("online", None)
            self.rank = self.json.get("rank", None)

    def __str__(self):
        return str(self.json)