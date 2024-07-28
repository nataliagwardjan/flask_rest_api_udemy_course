from book_library_app import db
from flask import jsonify, abort
from webargs.flaskparser import use_args
from book_library_app.models import Author, AuthorSchema, author_schema, Book, BookSchema, book_schema
from book_library_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, \
    get_pagination
from book_library_app.books import books_bp


@books_bp.route('/books', methods=['GET'])
def get_books():
    query = Book.query

    schema_args = get_schema_args(Book)
    query = apply_order(Book, query)
    query = apply_filter(Book, query)
    items, pagination = get_pagination(query, "books.get_books")
    books = BookSchema(**schema_args).dump(items)

    response = {
        "success": True,
        "data": books,
        "number_of_records": len(books),
        "pagination": pagination
    }

    return jsonify(response)


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    book = Book.query.get_or_404(book_id, description=f"Book with id {book_id} not found")
    response = {
        "success": True,
        "data": book_schema.dump(book)
    }

    return jsonify(response)


@books_bp.route('/authors/<int:author_id>/books', methods=['GET'])
def get_all_author_books(author_id: int):
    Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")
    books = Book.query.filter(Book.author_id == author_id).all()
    items = BookSchema(many=True, exclude=["author"]).dump(books)

    response = {
        "success": True,
        "data": items,
        "number_of_records": len(books)
    }

    return jsonify(response)


@books_bp.route('/authors/<int:author_id>/books', methods=['POST'])
@validate_json_content_type
@use_args(BookSchema(exclude=["author_id"]), error_status_code=400)
def create_book(args: dict, author_id: int):
    Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")
    if Book.query.filter(Book.isbn == args["isbn"]).first():
        abort(409, description=f"Book with ISBN {args['isbn']} already exist")

    book = Book(author_id=author_id, **args)

    db.session.add(book)
    db.session.commit()

    response = {
        "success": True,
        "data": book_schema.dump(book)
    }

    return jsonify(response), 201


@books_bp.route('/books/<int:book_id>', methods=['PUT'])
@validate_json_content_type
@use_args(book_schema, error_status_code=400)
def update_book(args: dict, book_id: int):
    book = Book.query.get_or_404(book_id, description=f"Book with id {book_id} not found")

    book_isbn = Book.query.filter(Book.isbn == args["isbn"]).first()
    if book_isbn and book_isbn.id != book_id:
        abort(409, description=f"Book with ISBN {args['isbn']} already exist")

    book.title = args["title"]
    book.isbn = args["isbn"]
    description = args["description"]
    if description is not None:
        book.description = description
    author_id = args["author_id"]
    if author_id is not None:
        Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")
        book.author_id = author_id
    book.number_of_pages = args["number_of_pages"]

    db.session.commit()

    response = {
        "success": True,
        "data": book_schema.dump(book)
    }

    return jsonify(response)


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id: int):
    book = Book.query.get_or_404(book_id, description=f"Book with id {book_id} not found")

    db.session.delete(book)
    db.session.commit()

    response = {
        "success": True,
        "data": f"Delete book with id {book_id}"
    }

    return jsonify(response)
