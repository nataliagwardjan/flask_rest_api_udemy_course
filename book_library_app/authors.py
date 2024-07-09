from book_library_app import app
from flask import jsonify


@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    response = {
        "success": True,
        "data": "Get all authors"
    }

    return jsonify(response)


@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    response = {
        "success": True,
        "data": f"Get author author with id {author_id}"
    }

    return jsonify(response)


@app.route('/api/v1/authors', methods=['POST'])
def create_author():
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
