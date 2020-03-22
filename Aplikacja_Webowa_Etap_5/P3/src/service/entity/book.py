import json


class Book:
    def __init__(self, id, author_id, title, year, filename=None, filepath=None):
        self.id = id
        self.author_id = author_id
        self.title = title
        self.year = year
        self.filename = filename
        self.filepath = filepath

    @classmethod
    def from_json(cls, data):
        return cls(**data)
