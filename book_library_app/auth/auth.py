from book_library_app.auth import auth_bp
from book_library_app.utils import validate_json_content_type, token_required
from webargs.flaskparser import use_args
from book_library_app.models import user_schema, User, UserSchema
from flask import jsonify, abort
from book_library_app import db


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args["username"]).first():
        abort(409, description=f"User with username {args['username']} already exist")
    if User.query.filter(User.email == args["email"]).first():
        abort(409, description=f"User with email {args['email']} already exist")

    args["password"] = User.generate_hashed_password(args["password"])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()

    response = {
        "success": True,
        "token": token
    }

    return jsonify(response)


@auth_bp.route('/login', methods=['POST'])
@validate_json_content_type
@use_args(UserSchema(only=["username", "password"]), error_status_code=400)
def login(args: dict):
    user = User.query.filter(User.username == args["username"]).first()

    if not user:
        abort(401, description=f"Invalid credentials")

    if not user.is_password_valid(args["password"]):
        abort(401, description=f"Invalid credentials")

    token = user.generate_jwt()

    response = {
        "success": True,
        "token": token
    }

    return jsonify(response)


@auth_bp.route('/me', methods=['GET'])
@token_required
@validate_json_content_type
@use_args(UserSchema(only=["username", "password"]), error_status_code=400)
def get_current_user(user_id: str, args: dict):
    user = User.query.get_or_404(user_id, description=f"User with id {user_id} not found")
    response = {
        "success": True,
        "data": user_schema.dump(user)
    }

    return jsonify(response)
