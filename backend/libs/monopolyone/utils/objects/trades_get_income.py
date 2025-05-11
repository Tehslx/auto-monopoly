from .users_get import UsersGet


class TradesGetIncome:
    
    def __init__(self, data: dict):
        self.json = data
        self.trades = None
        self.users_data = UsersGet(None)
        self.thing_types = None
        self.qualities = None
        self.collections = None
        self.item_ids_equipped = None

    @property
    def TradesGetIncome(self):
        self.trades = self.json.get("trades", None)
        self.users_data = UsersGet(self.json.get("users_data", {})).UsersGet
        self.thing_types = self.json.get("id_last", None)
        self.qualities = self.json.get("qualities", None)
        self.collections = self.json.get("collections", None)
        self.item_ids_equipped = self.json.get("item_ids_equipped", None)

        return self

    def __str__(self):
        return str(self.json)