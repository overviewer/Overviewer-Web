from flask import make_response
import functools

# decorator to set mime types
def content_type(mime_type, charset=None):
    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            r = make_response(f(*args, **kwargs))
            r.mimetype = mime_type
            if charset:
                r.charset = charset
            return r
        return inner
    return wrapper
