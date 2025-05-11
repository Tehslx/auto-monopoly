from .friends_get import FriendsGet
from .users_get import UsersGet
from .room_patch import RoomPatch
from .message import Message

class InfoGet:

    def __init__(self, data: dict):
        self.json = data
        self.seasonpass = None
        self.friends = FriendsGet(None)
        self.streams = None
        self.blog = None
        self.top_week = None
        self.missions = None
        self.gchat = Gchat(None)
        self.rooms = None
        self.users_data_rooms = UsersGet(None)

    @property
    def InfoGet(self):
        self.seasonpass = self.json.get("seasonpass", None)
        self.friends = FriendsGet(self.json.get("friends", None)).FriendsGet
        self.streams = self.json.get("streams", None)
        self.blog = self.json.get("blog", None)
        self.top_week = self.json.get("top_week", None)
        self.missions = self.json.get("missions", None)
        self.gchat = Gchat(self.json.get("gchat", None))
        self.rooms = self.json.get("rooms", {}).get("rooms", None)
        self.users_data_rooms = UsersGet(self.json.get("rooms", {}).get("users_data", None)).UsersGet

        for index, mission in enumerate(map(Missions, self.missions), start=1):
            setattr(self, f"mission_{index}", mission)
            if index == 1: 
                self.mission_1 = mission 
            elif index == 2: 
                self.mission_2 = mission 
            elif index == 3: 
                self.mission_3 = mission 
            elif index == 4: 
                self.mission_4 = mission 
            elif index == 5: 
                self.mission_5 = mission 


        for index, room in enumerate(map(RoomPatch, self.rooms), start=1):
            setattr(self, f"room_{index}", room)
            if index == 1: 
                self.room_1 = room 
            elif index == 2: 
                self.room_2 = room 
            elif index == 3: 
                self.room_3 = room 
            elif index == 4: 
                self.room_4 = room 
            elif index == 5: 
                self.room_5 = room 
        
        return self

    def __getattr__(self, data):
        if data.startswith("mission_"):
            return Missions(None)
        if data.startswith("room_"):
            return RoomPatch(None)   
    
    def __str__(self):
        return str(self.json)


class Missions:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.name = None
            self.counter = None
            self.target = None
            self.reward = None
            self.reward_type = None
            self.ts_expire = None
        else:
            self.json = data
            self.name = self.json.get("name", None)
            self.counter = self.json.get("counter", None)
            self.target = self.json.get("target", None)
            self.reward = self.json.get("reward", None)
            self.reward_type = self.json.get("reward_type", None)
            self.ts_expire = self.json.get("ts_expire", None)

    def __str__(self):
        return str(self.json)


class Gchat:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.messages = None
            self.item_protos = None
            self.users = None
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