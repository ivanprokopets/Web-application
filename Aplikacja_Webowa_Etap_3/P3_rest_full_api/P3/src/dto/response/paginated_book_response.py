from flask import jsonify
import json
from flask import Flask

app = Flask(__name__)


class PaginatedBookResponse:
    def __init__(self, books, start, limit, count):
        self.books = []

        for book in books:
            self.books.append(book.__dict__)

        self.start = start
        self.limit = limit
        self.current_size = len(books)
        self.count = count

    def get_json(self, url):
        if self.start <= 1:
            previous_url = ""
        else:
            start_previous = max(1, self.start - self.limit)
            previous_url = "{0}?start={1}&limit={2}".format(url, start_previous, self.limit)

        if self.start + self.limit > self.count:
            next_url = ""
        else:
            start_next = self.start + self.limit
            next_url = "{0}?start={1}&limit={2}".format(url, start_next, self.limit)
        app.logger.debug("Found {0} books.".format(self.books))
        return {
            "books": self.books,
            "start": self.start,
            "limit": self.limit,
            "current_size": self.current_size,
            "count": self.count,
            "previous": previous_url,
            "next": next_url
        }
