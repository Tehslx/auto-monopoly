from .users_get import User


class StreamsGetLive:
    
    def __init__(self, data: dict):
        self.json = data

    @property
    def StreamsGetLive(self):
        for index, stream in enumerate(map(StreamsLive, self.json), start=1):
            setattr(self, f"stream_{index}", stream)
            if index == 1: 
                self.stream_1 = stream 
            elif index == 2: 
                self.stream_2 = stream 
            elif index == 3: 
                self.stream_3 = stream 
            elif index == 4: 
                self.stream_4 = stream 
            elif index == 5: 
                self.stream_5 = stream 
        
        return self

    def __getattr__(self, data):
        if data.startswith("stream_"):
            return StreamsLive(None)    
    
    def __str__(self):
        return str(self.json)    
    

class StreamsLive:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.streams = Stream(None)
            self.user_data = User(None)
        else:
            self.json = data
            self.streams = Stream(self.json.get("streams", None)[0])
            self.user_data = User(self.json.get("user_data", None))
    
    def __str__(self):
        return str(self.json)


class Stream:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.platform = None
            self.platform_user = PlatformUser(None)
            self.title = None
            self.preview = Preview(None)
            self.viewers = None
        else:
            self.json = data
            self.platform = self.json.get("platform", None)
            self.platform_user = PlatformUser(self.json.get("platform_user", None))
            self.title = self.json.get("title", None)
            self.preview = Preview(self.json.get("preview", None))
            self.viewers = self.json.get("viewers", None)

    def __str__(self):
        return str(self.json)


class PlatformUser:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.id = None
            self.name = None
            self.display_name = None
        else:
            self.json = data
            self.id = self.json.get("id", None)
            self.name = self.json.get("name", None)
            self.display_name = self.json.get("display_name", None)

    def __str__(self):
        return str(self.json)


class Preview:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.large = None
            self.medium = None
        else:
            self.json = data
            self.large = self.json.get("large", None)
            self.medium = self.json.get("medium", None)

    def __str__(self):
        return str(self.json)