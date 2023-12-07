from functools import wraps

from pyverify import Verify
from pyverify import msg
from pyverify.exc import ValidationError


def patch(rules: dict):
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
            from flask import request  # noqa
            data = dict()
            data.update(request.args.to_dict())
            data.update(request.form.to_dict())
            if request.is_json:
                data = request.json
                if not isinstance(data, dict):
                    raise ValidationError(msg.Message.params.format(data=data, func_name=func.__name__))
            verified = Verify(data=data, rules=rules)
            result = func(*args, **kwargs, params=verified.params)
            return result

        return inner

    return wrapper
