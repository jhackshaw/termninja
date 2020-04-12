import json
from datetime import datetime
from sanic.exceptions import abort


def validate_page(request_page):
    try:
        page = int(request_page)
        if page < 0:
            page = 0
        return page
    except ValueError:
        abort(400, 'invalid page')


def serialize_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def serialize(value):
    return json.dumps(value, default=serialize_default)
