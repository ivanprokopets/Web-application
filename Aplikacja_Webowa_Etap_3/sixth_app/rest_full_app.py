from flask import Flask, request
from flask_restplus import Api, Resource, fields
from src.dto.request.book_request import BookRequest
from src.dto.request.author_request import AuthorRequest
from src.service.book_service import BookService
from src.service.author_service import AuthorService
from src.exception.exception import BookAlreadyExistsException, AuthorAlreadyExistsException, AuthorNotFoundByIdException

app = Flask(__name__)
api_app = Api(app = app, version = "0.1", title = "Sixth app API", description = "REST-full API for library")

hello_namespace = api_app.namespace("hello", description = "Info API")
author_namespace = api_app.namespace("author", description = "Author API")
book_namespace = api_app.namespace("book", description = "Book API")

START = "start"
LIMIT = "limit"

@hello_namespace.route("/")
class Hello(Resource):

    @api_app.doc(responses = {200: "OK, Hello World"})
    def get(self):
        return {
                "message": "Hello, World!"
        }

@author_namespace.route("/")
class Author(Resource):

    def __init__(self, args):
        super().__init__(args)
        self.author_service = AuthorService()

    new_author_model = api_app.model("Author model",
            {
                "name": fields.String(required = True, description = "Author name", help = "Name cannot be blank"),
                "surname": fields.String(required = True, description = "Author surname", help = "Surname cannot be null")
            })

    @api_app.expect(new_author_model)
    def post(self):
        try:
            author_req = AuthorRequest(request)
            saved_author_id = self.author_service.add_author(author_req)

            result = {"message": "Added new author", "save_author_id": saved_author_id}

            return result

        except AuthorAlreadyExistsException as e:
            author_namespace.abort(409, e.__doc__, status = "Could not save author. Already exists", statusCode= 409)


@book_namespace.route("/<int:id>")
class Book(Resource):

    @api_app.doc(responses = {200: "OK", 400: "Invalid argument"},
            params = {"id": "Specify book Id"})
    def get(self, id):
        try:

            return {
                    "message": "Found book by id: {0}".format(id)
            }

        except Exception as e:
            book_namespace.abort(400, e.__doc__, status = "Could not find book by id", statusCode = "400")

    @api_app.doc(responses = {200: "OK", 400: "Invalid argument"},
            params = {"id": "Specify book Id to remove"})
    def delete(self, id):
        try:

            return {
                    "message": "Removed book by id: {0}".format(id)
            }

        except Exception as e:
            book_namespace.abort(400, e.__doc__, status = "Could not remove book by id", statusCode = "400")

@book_namespace.route("/list")
class BookList(Resource):

    def __init__(self, args):
        super().__init__(args)
        self.book_service = BookService()
        self.author_service = AuthorService()

    new_book_model = api_app.model("Book model",
            {
                "title": fields.String(required = True, description = "Book title", help = "Title cannot be null", example = "Bieguni"),
                "year": fields.Integer(required = True, description = "Year of publication", help = "Year cannot be null", example = "2007"),
                "author_id": fields.Integer(required = True, description = "Author's Id ", help = "Author's Id cannot be null")
            })

    @api_app.param(START, "The data will be returned from this position.")
    @api_app.param(LIMIT, "The max size of returned data.")
    @api_app.doc(responses = {200: "OK"})
    def get(self):
        start = self.parse_request_arg_or_zero(request, START, "0")
        start = max(1, start)
        limit = self.parse_request_arg_or_zero(request, LIMIT, "50")

        paginated_book_response = self.book_service.get_paginated_books_response(start, limit)

        return paginated_book_response.get_json(request.base_url)

    def parse_request_arg_or_zero(self, request, param, default_value):
        val = request.args.get(param, default_value)
        val = int(val) if val.isdigit() else 0
        return val

    @api_app.expect(new_book_model)
    def post(self):
        try:
            book_req = BookRequest(request)
            author = self.author_service.get_author_by_id(book_req.author_id)
            saved_book_id = self.book_service.add_book(book_req)

            result = {"message": "Added new book", "saved_book_id": saved_book_id}

            return result

        except KeyError as e:
            book_namespace.abort(400, e.__doc__, status = "Could not save new book", statusCode = "400")

        except BookAlreadyExistsException as e:
            book_namespace.abort(409, e.__doc__, status = "Could not save new book. Already exists", statusCode = "409")

        except AuthorNotFoundByIdException as e:
            book_namespace.abort(404, e.__doc__, status = "Could not save new book. Author (by id) does not exist.", statusCode = "404")