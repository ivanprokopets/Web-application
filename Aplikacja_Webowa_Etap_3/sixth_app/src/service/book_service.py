from flask import Flask
from src.service.repositories.book_repository import BookRepository
from src.dto.response.paginated_book_response import PaginatedBookResponse

app = Flask(__name__)

class BookService:

    def __init__(self):
        self.book_repo = BookRepository()

    def add_book(self, book_req):
        app.logger.debug("Adding book...")
        book_id = self.book_repo.save(book_req)
        app.logger.debug("Added book (id: {0})".format(book_id))
        return book_id

    def get_paginated_books_response(self, start, limit):
        app.logger.debug("Getting paginated books (start: {0}, limit: {1})".format(start, limit))
        n_of_books = self.book_repo.count_all()

        books = self.book_repo.find_n_books(start, limit)

        books_response = PaginatedBookResponse(books, start, limit, n_of_books)

        app.logger.debug("Got paginated books (start: {0}, limit: {1}, count: {2}, current_size: {3})".format(start, limit, n_of_books, len(books)))
        return books_response