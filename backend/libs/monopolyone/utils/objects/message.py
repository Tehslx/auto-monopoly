class Message:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.msg_id = None
            self.text = None
            self.ts = None
            self.type = None
            self.user_id = None
            self.user_ids_mentioned = None
        else:
            self.json = data
            self.msg_id = self.json.get("msg_id", None)
            self.text = self.json.get("text", None)
            self.ts = self.json.get("ts", None)
            self.type = self.json.get("type", None)
            self.user_id = self.json.get("user_id", None)
            self.user_ids_mentioned = self.json.get("user_ids_mentioned", None)
    
    def __str__(self):
        return str(self.json)