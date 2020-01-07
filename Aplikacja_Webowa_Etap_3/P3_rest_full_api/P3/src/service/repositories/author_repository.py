from flask import Flask
import redis
import json

from ...service.entity.author import Author
from ...exception.exception import AuthorAlreadyExistsException

app = Flask(__name__)

AUTHOR_COUNTER = "author_counter"
AUTHOR_ID_PREFIX = "author_"


class AuthorRepository:

    def __init__(self):
        self.db = redis.Redis(host="redis", port=6379, decode_responses=True)
        if self.db.get(AUTHOR_COUNTER) == None:
            self.db.set(AUTHOR_COUNTER, 0)

    def save(self, author_req):
        app.logger.debug("Saving new author: {0}.".format(author_req))
        author = self.find_by_names(author_req.name, author_req.surname)

        if author != None:
            raise AuthorAlreadyExistsException(
                "Author (name: \"{0}\", surname: \"{1}\") already exists".format(author_req.name, author_req.surname))

        author = Author(self.db.incr(AUTHOR_COUNTER), author_req.name, author_req.surname)

        author_id = AUTHOR_ID_PREFIX + str(author.id)
        author_json = json.dumps(author.__dict__)

        self.db.set(author_id, author_json)

        app.logger.debug("Saved new author: (id: {0}).".format(author.id))
        return author.id

    def delete(self, id):
        app.logger.debug("START DELETE AUTHOR in repo")
        self.db.delete(AUTHOR_ID_PREFIX + str(id))
        return True

    def find_by_names(self, name, surname):
        n = int(self.db.get(AUTHOR_COUNTER))

        for i in range(1, n + 1):
            author_id = AUTHOR_ID_PREFIX + str(i)

            if not self.db.exists(author_id):
                continue

            author_json = self.db.get(author_id)
            author = Author.from_json(json.loads(author_json))

            if author.name == name and author.surname == surname:
                return author

        return None

    def find_by_id(self, author_id_to_find):
        n = int(self.db.get(AUTHOR_COUNTER))

        for i in range(1, n + 1):
            author_id = AUTHOR_ID_PREFIX + str(i)

            if not self.db.exists(author_id):
                continue

            author_json = self.db.get(author_id)
            author = Author.from_json(json.loads(author_json))
            app.logger.debug("ID: {0}.".format(type(author.id)))
            if author.id == author_id_to_find:
                return author

        return None

    def find_n_authors(self):
        app.logger.debug("Finding all books")
        n = int(self.db.get(AUTHOR_COUNTER))
        authors = []
        authorsjson = []
        for i in range(1, n + 1):

            author_id = AUTHOR_ID_PREFIX + str(i)

            if not self.db.exists(author_id):
                continue

            author_json = self.db.get(author_id)
            author = Author.from_json(json.loads(author_json))

            authors.append(author)

        app.logger.debug("Found {0} books.".format(authors))
        for i in authors:
            authorsjson.append(i.__dict__)
        return authorsjson
