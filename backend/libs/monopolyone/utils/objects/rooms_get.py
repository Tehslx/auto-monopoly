from .room_patch import RoomPatch
from .users_get import UsersGet

class RoomsGet:

    def __init__(self, data: dict):
        self.json = data
        self.rooms = None
        self.users_data_rooms = None

    @property
    def RoomsGet(self):
        self.rooms = self.json.get("rooms", None)
        self.users_data_rooms = UsersGet(self.json.get("users_data", None)).UsersGet

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
        if data.startswith("room_"):
            return RoomPatch(None)   
    
    def __str__(self):
        return str(self.json)