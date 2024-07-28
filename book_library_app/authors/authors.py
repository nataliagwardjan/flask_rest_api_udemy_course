from book_library_app import db
from flask import jsonify
from webargs.flaskparser import use_args
from book_library_app.models import Author, AuthorSchema, author_schema
from book_library_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, \
    get_pagination
from book_library_app.authors import authors_bp


@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    query = Author.query

    schema_args = get_schema_args(Author)
    query = apply_order(Author, query)
    query = apply_filter(Author, query)
    items, pagination = get_pagination(query, "authors.get_authors")
    authors = AuthorSchema(**schema_args).dump(items)

    response = {
        "success": True,
        "data": authors,
        "number_of_records": len(authors),
        "pagination": pagination
    }

    return jsonify(response)


@authors_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")
    response = {
        "success": True,
        "data": author_schema.dump(author)
    }

    return jsonify(response)


@authors_bp.route('/authors', methods=['POST'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def create_author(body: dict):
    author = Author(**body)

    db.session.add(author)
    db.session.commit()
    response = {
        "success": True,
        "data": author_schema.dump(author)
    }

    return jsonify(response), 201


@authors_bp.route('/authors/<int:author_id>', methods=['PUT'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def update_author(args: dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")

    author.first_name = args["first_name"]
    author.second_name = args["second_name"]
    author.birth_date = args["birth_date"]

    db.session.commit()

    response = {
        "success": True,
        "data": author_schema.dump(author)
    }

    return jsonify(response)


@authors_bp.route('/authors/<int:author_id>', methods=['DELETE'])
def remove_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")

    db.session.delete(author)
    db.session.commit()

    response = {
        "success": True,
        "data": f"Delete author with id {author_id}"
    }

    return jsonify(response)
