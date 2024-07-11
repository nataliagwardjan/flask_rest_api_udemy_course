from book_library_app import app, db
from flask import jsonify, request
from webargs.flaskparser import use_args
from book_library_app.models import Author, AuthorSchema, author_schema
from book_library_app.utils import validate_json_content_type


@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    response = {
        "success": True,
        "data": author_schema.dump(authors),
        "number_of_records": len(authors)
    }

    return jsonify(response)


@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")
    response = {
        "success": True,
        "data": author_schema.dump(author)
    }

    return jsonify(response)


@app.route('/api/v1/authors', methods=['POST'])
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def create_author(body: dict):
    author = Author(**body)
    print(author)
    db.session.add(author)
    db.session.commit()
    response = {
        "success": True,
        "data": author_schema.dump(author)
    }

    return jsonify(response), 201


@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id: int):
    response = {
        "success": True,
        "data": f"Update author author with id {author_id}"
    }

    return jsonify(response)


@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
def remove_author(author_id: int):
    response = {
        "success": True,
        "data": f"Delete author with id {author_id}"
    }

    return jsonify(response)
