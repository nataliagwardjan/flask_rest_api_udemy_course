from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps
from book_library_app import db
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression
import re
from flask_sqlalchemy.query import Query
from flask import request, url_for, current_app

from config import Config

COMPARISON_OPERATORS_RE = re.compile(r"(.*)\[(gt|gte|lt|lte)\]")


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)
        if data is None:
            raise UnsupportedMediaType("Content type must be application/json")
        return func(*args, **kwargs)

    return wrapper


def get_schema_args(model: db.Model) -> dict:
    schema_args = {"many": True}
    fields = request.args.get("fields")
    if fields:
        schema_args["only"] = [field for field in fields.split(",") if field in model.__table__.columns]
    return schema_args


def apply_order(model: db.Model, query: Query) -> Query:
    sort_keys = request.args.get("sort")
    if sort_keys:
        for key in sort_keys.split(","):
            desc = False
            if key.startswith("-"):
                key = key[1:]
                desc = True
            column_attr = getattr(model, key, None)
            if column_attr is not None:
                query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)
    return query


def _get_filter_argument(column_name: InstrumentedAttribute, value: str, operator: str) -> BinaryExpression:
    operator_mapping = {
        "==": column_name == value,
        "gte": column_name >= value,
        "gt": column_name > value,
        "lte": column_name <= value,
        "lt": column_name < value
    }
    return operator_mapping[operator]


def apply_filter(model: db.Model, query: Query) -> Query:
    for param, value in request.args.items():
        if param not in {"field", "sort", "page", "limit"}:
            operator = "=="
            match = COMPARISON_OPERATORS_RE.match(param)
            if match is not None:
                param, operator = match.groups()
            column_attr = getattr(model, param, None)
            if column_attr is not None:
                value = model.additional_validation(param, value)
                if value is None:
                    continue
                filter_argument = _get_filter_argument(column_attr, value, operator)
                query = query.filter(filter_argument)
    return query


def get_pagination(query: Query, function_name: str) -> tuple[list, dict]:
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", current_app.config.get("PER_PAGE", 5), type=int)
    params = {key: value for key, value in request.args.items() if key != "page"}
    paginate_obj = query.paginate(page=page, per_page=limit, error_out=False)
    pagination = {
        "total_pages": paginate_obj.pages,
        "total_records": paginate_obj.total,
        "current_page": url_for(function_name, page=page, **params)
    }
    if paginate_obj.has_next:
        pagination["next_page"] = url_for(function_name, page=page + 1, **params)
    if paginate_obj.has_prev:
        pagination["previous_page"] = url_for(function_name, page=page - 1, **params)

    return paginate_obj.items, pagination
