from flask import Flask
from src.service.repositories.book_repository import BookRepository
from src.dto.response.paginated_book_response import PaginatedBookResponse
from src.exception.exception import BookNotFoundByIdException

app = Flask(__name__)


class BookService:

    def __init__(self):
        self.book_repo = BookRepository()

    def add_file_to_book(self, id, file):
        app.logger.debug("Adding book...")
        book_id = self.book_repo.save_file(id, file)
        app.logger.debug("Added book (id: {0})".format(book_id))
        return book_id

    def add_book(self, book_req):
        app.logger.debug("Adding book...")
        book_id = self.book_repo.save(book_req)
        app.logger.debug("Added book (id: {0})".format(book_id))
        return book_id

    def delete_book(self, id):
        book = self.book_repo.find_by_id(id)

        if book == None:
            raise BookNotFoundByIdException("Not found book by id: {0}".format(id))
        self.book_repo.delete(id)

    def delete_file_to_book(self, id):
        book = self.book_repo.find_by_id(id)

        if book.filename == None:
            raise BookNotFoundByIdException("Book with id {0} don't have file".format(id))
        self.book_repo.delete_file(id)

    def get_book_file(self, id):
        app.logger.debug("GET FILE")
        book = self.book_repo.find_by_id(id)

        if book.filename == None:
            raise BookNotFoundByIdException("Book with id {0} don't have file".format(id))

        return self.book_repo.download_file(id)

    def clear_author_books(self, author_id):
        app.logger.debug("START DELETE BOOKS FOR AUTHOR_ID")
        self.book_repo.delete_books_for_authorID(author_id)
        return True

    def get_paginated_books_response(self, start, limit):
        app.logger.debug("Getting paginated books (start: {0}, limit: {1})".format(start, limit))
        n_of_books = self.book_repo.count_all()

        books = self.book_repo.find_n_books(start, limit)

        books_response = PaginatedBookResponse(books, start, limit, n_of_books)

        app.logger.debug(
            "Got paginated books (start: {0}, limit: {1}, count: {2}, current_size: {3})".format(start, limit,
                                                                                                 n_of_books,
                                                                                                 len(books)))
        return books_response

    def get_book_by_id(self, book_id):
        app.logger.debug("Getting book by id: {0}.".format(book_id))
        book = self.book_repo.find_by_id(book_id)

        if book == None:
            raise BookNotFoundByIdException("Not found book by id: {0}".format(book_id))

        app.logger.debug("Got author by id: {0}".format(book_id))
        return book
