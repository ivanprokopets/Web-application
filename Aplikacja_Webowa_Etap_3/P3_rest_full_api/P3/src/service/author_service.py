from flask import Flask
from src.service.repositories.author_repository import AuthorRepository
from src.exception.exception import AuthorNotFoundByIdException

app = Flask(__name__)


class AuthorService:

    def __init__(self):
        self.author_repo = AuthorRepository()

    def add_author(self, author_req):
        app.logger.debug("Adding author...")
        author_id = self.author_repo.save(author_req)
        app.logger.debug("Added author (id: {0})".format(author_id))
        return author_id

    def delete_author_by_id(self, author_id):
        app.logger.debug("START DELETE AUTHOR in service")
        self.author_repo.delete(author_id)
        return True

    def get_author_by_id(self, author_id):
        app.logger.debug("Getting author by id: {0}.".format(author_id))

        author = self.author_repo.find_by_id(author_id)

        if author == None:
            raise AuthorNotFoundByIdException("Not found author by id: {0}".format(author_id))

        app.logger.debug("Got author by id: {0}".format(author_id))
        return author

    def get_paginated_authors_response(self):
        authors = self.author_repo.find_n_authors()
        result = {
            "authors": authors
        }

        return result
