from .message import Message
from .users_get import UsersGet

class GchatGet:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.messages = None
            self.item_protos = None
            self.users = UsersGet(None)
        else:
            self.json = data
            self.messages = self.json.get("messages", None)
            self.item_protos = self.json.get("item_protos", None)
            self.users = UsersGet(self.json.get("users", None)).UsersGet


            for index, item_proto in enumerate(map(ItemProtosGchat, self.item_protos), start=1):
                setattr(self, f"item_proto_{index}", item_proto)
                if index == 1: 
                    self.item_proto_1 = item_proto 
                elif index == 2: 
                    self.item_proto_2 = item_proto
                elif index == 3: 
                    self.item_proto_3 = item_proto
                elif index == 4: 
                    self.item_proto_4 = item_proto
                elif index == 5: 
                    self.item_proto_5 = item_proto


            for index, message in enumerate(map(Message, self.messages), start=1):
                setattr(self, f"message_{index}", message)
                if index == 1: 
                    self.message_1 = message 
                elif index == 2: 
                    self.message_2 = message 
                elif index == 3: 
                    self.message_3 = message 
                elif index == 4: 
                    self.message_4 = message 
                elif index == 5: 
                    self.message_5 = message 

    def __getattr__(self, data):
        if data.startswith("item_proto_"):
            return ItemProtosGchat(None)
        if data.startswith("message_"):
            return Message(None)  
    
    def __str__(self):
        return str(self.json)


class ItemProtosGchat:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.item_proto_id = None
            self.type = None
            self.image = None
            self.title = None
            self.description = None
            self.quality_id = None
        else:
            self.json = data
            self.item_proto_id = self.json.get("item_proto_id", None)
            self.type = self.json.get("type", None)
            self.image = self.json.get("image", None)
            self.title = self.json.get("title", None)
            self.description = self.json.get("description", None)
            self.quality_id = self.json.get("quality_id", None)

    def __str__(self):
        return str(self.json)