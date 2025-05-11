from .current_game import CurrentGame

class AccountInfo:

    def __init__(self, data: dict):
        self.json = data
        self.user_id = None
        self.domain = None
        self.approved = None
        self.nickname = None
        self.nicks_old = []
        self.profile_cover = None
        self.social_vk = None
        self.gender = None
        self.avatar = None
        self.avatar_key = None
        self.online = None
        self.current_game = CurrentGame(None)
        self.rank = None
        self.vip = None
        self.bot = None
        self.bot_owner = None
        self.moderator = None
        self.games = None
        self.games_wins = None
        self.xp = None
        self.xp_level = None
        self.badge = None
        self.friendship = None
        self.muted = None
        self.mfp_ban_history = None
        self.admin_rights = None
        self.penalties = None
        self.balance = None
        self.email = None
        self.email_verified = None
        self.hasPassword = None
        self.hasTotp = None
        self.social = None
        self.vip_free_allowed = None

    @property
    def AccountInfo(self):
        self.user_id = self.json.get("user_id", None)
        self.domain = self.json.get("domain", None)
        self.approved = self.json.get("approved", None)
        self.nickname = self.json.get("nick", None)
        self.nicks_old = self.json.get("nicks_old", [])
        self.profile_cover = self.json.get("profile_cover", None)
        self.social_vk = self.json.get("social_vk", None)
        self.gender = self.json.get("gender", None)
        self.avatar = self.json.get("avatar", None)
        self.avatar_key = self.json.get("avatar_key", None)
        self.online = self.json.get("online", None)
        self.current_game = CurrentGame(self.json.get("current_game", None))
        self.rank = self.json.get("rank", None)
        self.vip = self.json.get("vip", None)
        self.bot = self.json.get("bot", None)
        self.bot_owner = self.json.get("bot_owner", None)
        self.moderator = self.json.get("moderator", None)
        self.games_wins = self.json.get("games_wins", None)
        self.games = self.json.get("games", None)
        self.xp = self.json.get("xp", None)
        self.xp_level = self.json.get("xp_level", None)
        self.badge = self.json.get("badge", None)
        self.friendship = self.json.get("friendship", None)
        self.muted = self.json.get("muted", None)
        self.mfp_ban_history = self.json.get("mfp_ban_history", None)
        self.admin_rights = self.json.get("admin_rights", None)
        self.penalties = self.json.get("penalties", {})
        self.balance = self.json.get("balance", None)
        self.email = self.json.get("email", None)
        self.email_verified = self.json.get("email_verified", None)
        self.hasPassword = self.json.get("hasPassword", None)
        self.hasTotp = self.json.get("hasTotp", None)
        self.social = self.json.get("social", {})
        self.vip_free_allowed = self.json.get("vip_free_allowed", None)   
        return self

    def __str__(self):
        return str(self.json)