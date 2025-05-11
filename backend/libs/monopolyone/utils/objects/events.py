from .im_sync import ImSync
from .room_patch import RoomPatch
from .global_chat_add import GlobalChatAdd
from .message import Message
from .users_data import UsersData

class Events:

    def __init__(self, data: dict):
        self.json = data
        self.events = []
        self.rooms = []
        self.users_data = []
        self.messages = []

    @property
    def Events(self):
        for event in self.json.get("events", []):
            if event.get("type") in ["room.delete", "room.set"]:
                self.events.append(RoomPatch(event))
            elif event.get("type") == "im.sync":
                self.events.append(ImSync(event).ImSync)
            elif event.get("type") == "room.patch":
                self.events.append(RoomPatch(event))
            elif event.get("type") == "gchat.add":
                self.events.append(GlobalChatAdd(event).GlobalChatAdd)
                for message in self.json.get("messages", []):
                    self.messages.append(Message(message).Message)
        for user in self.json.get("users_data", []):
            self.users_data.append(UsersData(user).UsersData)
        return self