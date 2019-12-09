import json

class Author:
    def __init__(self, id, name, surname):
        self.id = id
        self.name = name
        self.surname = surname

    @classmethod
    def from_json(cls, data):
        return cls(**data)