from functools import wraps

from pyverify import Verify


def assign(rules: dict):
    """Parameter check decorator for flask.

    How to use?

        from flask import Flask, request

        from pyverify.frame.flask import assign
        from pyverify.verify import rule, phone

        app = Flask(__name__)

        params = {
            'telephone': rule(phone),
            'isEo': rule(bool),
        }

        @app.route("/index")
        @assign(params)
        def index():
            ...

    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from flask import request  # noqa
            if request.is_json:
                data = request.json
                many = True if isinstance(data, list) else False
            else:
                data = dict()
                data.update(request.args.to_dict())
                data.update(request.form.to_dict())
                many = False
            verified = Verify(data=data, rules=rules, many=many)
            result = func(*args, **kwargs, params=verified.params)
            return result

        return inner

    return wrapper
