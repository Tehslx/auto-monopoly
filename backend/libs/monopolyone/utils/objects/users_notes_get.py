from .users_get import UsersGet


class UsersNotesGet:
    
    def __init__(self, data: dict):
        self.json = data
        self.count = None
        self.notes = None
        self.users_data = UsersGet(None)

    @property
    def UsersNotesGet(self):
        self.count = self.json.get("count", None)
        self.notes = self.json.get("notes", [])
        self.users_data = UsersGet(self.json.get("users_data", {})).UsersGet


        for index, note in enumerate(map(Notes, self.notes), start=1):
            setattr(self, f"note_{index}", note)
            if index == 1: 
                self.note_1 = note 
            elif index == 2: 
                self.note_2 = note 
            elif index == 3: 
                self.note_3 = note 
            elif index == 4: 
                self.note_4 = note 
            elif index == 5: 
                self.note_5 = note
        
        return self
    
    def __getattr__(self, data):
        if data.startswith("note_"):
            return Notes(None)
    
    def __str__(self):
        return str(self.json)


class Notes:
    
    def __init__(self, data: dict):
        if not data:
            self.json = None
            self.user_id = None
            self.user_id_about = None
            self.text = None
        else:
            self.json = data
            self.user_id = self.json.get("user_id", None)
            self.user_id_about = self.json.get("user_id_about", None)
            self.text = self.json.get("text", None)

    def __str__(self):
        return str(self.json)