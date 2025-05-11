class RoomPatch:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.id = None
            self.patches = []
            self.room_id = None
            self.type = None
            self.v = None
            self.reason = None
            self.status = None
            self.game_mode = None
            self.game_submode = None
            self.game_2x2 = None
            self.admin = None
            self.players = None
            self.players_joined = None
            self.invites = None
            self.bans = None
            self.flags = Flags(None)
            self.settings = Settings(None)
            self.gsm_vote_variants = None
            self.gsm_votes = None
            self.op_ts_end = None
        else:
            self.json = data
            self.id = self.json.get("id", None)
            self.patches = self.json.get("patches", [])
            self.room_id = self.json.get("room_id", None)
            self.type = self.json.get("type", None)
            self.v = self.json.get("v", None)
            self.reason = self.json.get("reason", None)
            self.status = self.json.get("status", None)
            self.game_mode = self.json.get("game_mode", None)
            self.game_submode = self.json.get("game_submode", None)
            self.game_2x2 = self.json.get("game_2x2", None)
            self.admin = self.json.get("admin", None)
            self.players = self.json.get("players", None)
            self.players_joined = self.json.get("players_joined", None)
            self.invites = self.json.get("invites", None)
            self.bans = self.json.get("bans", None)
            self.flags = Flags(self.json.get("flags", None))
            self.settings = Settings(self.json.get("settings", None))
            self.gsm_vote_variants = self.json.get("gsm_vote_variants", None)
            self.gsm_votes = self.json.get("gsm_votes", None)
            self.op_ts_end = self.json.get("op_ts_end", None)

        player = None
        if not self.players:
            self.players = []
        for players_group in self.players:
            for index, player in enumerate(players_group, start=1):
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

        invite = None
        if not self.invites:
            self.invites = []
        for invites_group in self.invites: 
            for index, invite in enumerate(invites_group, start=1):
                setattr(self, f"invite_{index}", invite)
                if index == 1: 
                    self.invite_1 = invite
                elif index == 2: 
                    self.invite_2 = invite 
                elif index == 3: 
                    self.invite_3 = invite 
                elif index == 4: 
                    self.invite_4 = invite 
                elif index == 5: 
                    self.invite_5 = invite

            for index, ban in enumerate((self.bans), start=1):
                setattr(self, f"ban_{index}", invite)
                if index == 1: 
                    self.ban_1 = ban
                elif index == 2: 
                    self.ban_2 = ban 
                elif index == 3: 
                    self.ban_3 = ban 
                elif index == 4: 
                    self.ban_4 = ban 
                elif index == 5: 
                    self.ban_5 = ban

    def __getattr__(self, data):
        if data.startswith("player_"):
            return None
        if data.startswith("invite_"):
            return None 
        if data.startswith("ban_"):
            return None
    
    def __str__(self):
        return str(self.json)


class Flags:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.ts_created = None
            self.disposition_mode = None
            self.vip = None
            self.is_tournament = None
        else:
            self.json = data
            self.ts_created = self.json.get("ts_created", None)
            self.disposition_mode = self.json.get("disposition_mode", None)
            self.vip = self.json.get("vip", None)
            self.is_tournament = self.json.get("is_tournament", None)

    def __str__(self):
        return str(self.json)


class Settings:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.maxplayers = None
            self.private = None
            self.autostart = None
            self.game_timers = None
            self.br_corner = None
            self.restarts = None
            self.pm_allowed = None
            self.contract_protests = None
        else:
            self.json = data
            self.maxplayers = self.json.get("maxplayers", None)
            self.private = self.json.get("private", None)
            self.autostart = self.json.get("autostart", None)
            self.game_timers = self.json.get("game_timers", None)
            self.br_corner = self.json.get("br_corner", None)
            self.restarts = self.json.get("restarts", None)
            self.pm_allowed = self.json.get("pm_allowed", None)
            self.contract_protests = self.json.get("contract_protests", None)

    def __str__(self):
        return str(self.json)