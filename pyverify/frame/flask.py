from functools import wraps

from pyverify import Verify


def patch(rules: dict, many=False):
    """Parameter check decorator for flask.

    How to use?

        from flask import Flask, request

        from pyverify.frame.flask import patch
        from pyverify.verify import rule, phone

        app = Flask(__name__)

        params = {
            'telephone': rule(phone),
            'isEo': rule(bool),
        }

        @patch(params)
        @app.route("/index")
        def index():
            ...

    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            verified = Verify(data={}, rules=rules, many=many)
            result = func(*args, **kwargs, params=verified.params)
            return result

        return inner

    return wrapper
