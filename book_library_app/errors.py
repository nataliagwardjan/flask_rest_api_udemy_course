from book_library_app import app, db
from flask import Response, jsonify


class ErrorResponse:
    def __init__(self, message: str, http_status: int):
        self.payload = {
            "success": False,
            "message": message
        }
        self.http_status = http_status

    def to_response(self) -> Response:
        response = jsonify(self.payload)
        response.status_code = self.http_status
        return response


@app.errorhandler(404)
def not_found_error(err):
    return ErrorResponse(err.description, 404).to_response()


@app.errorhandler(400)
def bad_request_error(err):
    message = err.data.get("messages", {}).get("json", {})
    return ErrorResponse(message, 400).to_response()


@app.errorhandler(415)
def unsupported_media_type_error(err):
    return ErrorResponse(err.description, 415).to_response()


@app.errorhandler(500)
def internal_server_error(err):
    db.session.rollback()
    return ErrorResponse(err.description, 415).to_response()