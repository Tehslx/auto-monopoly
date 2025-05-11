class SessionGet:

    def __init__(self, data: dict):
        self.json = data
        self.user_id = None
        self.access_token = None
        self.expires = None
        self.expires_in = None
        self.refresh_token = None
        self.totp_session_token = None

    @property
    def SessionGet(self):
        self.user_id = self.json.get("user_id", None)
        self.access_token = self.json.get("access_token", None)
        self.expires = self.json.get("expires", None)
        self.expires_in = self.json.get("expires_in", None)
        self.refresh_token = self.json.get("refresh_token", None)
        self.totp_session_token = self.json.get("totp_session_token", None)
        return self

    def __str__(self):
        return str(self.json)