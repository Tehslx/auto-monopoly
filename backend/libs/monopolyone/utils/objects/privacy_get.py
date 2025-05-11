class PrivacyGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.trades_income = None
        self.trades_income_from_friends = None
        self.trades_income_gifts = None
        self.trades_income_gifts_autoaccept = None
        self.stream_autoplay = None

    @property
    def PrivacyGet(self):
        self.trades_income = self.json.get("trades_income", None)
        self.trades_income_from_friends = self.json.get("trades_income_from_friends", None)
        self.trades_income_gifts = self.json.get("trades_income_gifts", None)
        self.trades_income_gifts_autoaccept = self.json.get("trades_income_gifts_autoaccept", None)
        self.stream_autoplay = self.json.get("stream_autoplay", None)
        
        return self
    
    def __str__(self):
        return str(self.json)