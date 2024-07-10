from book_library_app import app, db
from flask import jsonify, request
from book_library_app.models import Author, AuthorSchema, author_schema


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
def create_author():
    body = request.get_json()
    first_name = body['first_name']
    second_name = body['second_name']
    birth_date = body['birth_date']
    author = Author(first_name=first_name, second_name=second_name, birth_date=birth_date)
    print(author)
    db.session.add(author)
    db.session.commit()
    response = {
        "success": True,
        "data": "New author has been created"
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
