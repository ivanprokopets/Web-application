import json

class Book:
    def __init__(self, id, author_id, title, year):
        self.id = id
        self.author_id = author_id
        self.title = title
        self.year = year

    @classmethod
    def from_json(cls, data):
        return cls(**data)