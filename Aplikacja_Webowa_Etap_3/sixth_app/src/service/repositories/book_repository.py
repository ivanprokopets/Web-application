from flask import Flask
import redis
import json

from ...service.entity.book import Book
from ...exception.exception import BookAlreadyExistsException

app = Flask(__name__)

BOOK_COUNTER = "book_counter"
BOOK_ID_PREFIX = "book_"

class BookRepository:

    def __init__(self):
        self.db = redis.Redis(host = "redis", port = 6379, decode_responses = True)
        if self.db.get(BOOK_COUNTER) == None:
            self.db.set(BOOK_COUNTER, 0)

    def save(self, book_req):
        app.logger.debug("Saving new book: {0}.".format(book_req))
        book = self.find_book_by_title(book_req.title)

        if book != None:
            raise BookAlreadyExistsException("Book title \"{0}\" already exist.".format(book_req.title))

        book = Book(self.db.incr(BOOK_COUNTER), book_req.author_id, book_req.title, book_req.year)

        book_id = BOOK_ID_PREFIX + str(book.id)
        book_json = json.dumps(book.__dict__)

        self.db.set(book_id, book_json)

        app.logger.debug("Saved new book: (id: {0}).".format(book.id))
        return book.id

    def find_book_by_title(self, title):
        n = int(self.db.get(BOOK_COUNTER))

        for i in range(1, n + 1):
            book_id = BOOK_ID_PREFIX + str(i)

            if not self.db.exists(book_id):
                continue

            book_json = self.db.get(book_id)
            book = Book.from_json(json.loads(book_json))

            if book.title == title:
                return book

        return None

    def count_all(self):
        app.logger.debug("Starting counting all books")
        n = int(self.db.get(BOOK_COUNTER))

        n_of_books = 0

        for i in range(1, n + 1):
            book_id = BOOK_ID_PREFIX + str(i)

            if self.db.exists(book_id):
                n_of_books += 1

        app.logger.debug("Counted all books (n: {0})".format(n_of_books))
        return n_of_books

    def find_n_books(self, start, limit):
        app.logger.debug("Finding n of books (start: {0}, limit: {1}".format(start, limit))
        n = int(self.db.get(BOOK_COUNTER))

        books = []
        counter = 1

        for i in range(1, n + 1):
            book_id = BOOK_ID_PREFIX + str(i)

            if not self.db.exists(book_id):
                continue

            if counter < start:
                counter += 1
                continue

            book_json = self.db.get(book_id)
            book = Book.from_json(json.loads(book_json))
            books.append(book)

            if len(books) >= limit:
                break

        app.logger.debug("Found {0} books.".format(len(books)))
        return books