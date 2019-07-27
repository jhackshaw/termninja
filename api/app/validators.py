from sanic.exceptions import abort


def validate_page(request_page):
    try:
        page = int(request_page)
        if page < 0:
            page = 0
        return page
    except ValueError:
        abort(400, 'invalid page')
