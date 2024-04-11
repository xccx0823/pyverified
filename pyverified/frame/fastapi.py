import asyncio
import json as pyjson
from dataclasses import dataclass
from functools import wraps
from typing import Optional

from pyverified import Verify


@dataclass
class Params:
    query = None
    form = None
    json = None
    headers = None


def with_request(
        *,
        query: Optional[dict] = None,
        form: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        many: bool = False):
    """Parameter check decorator for fastapi.

    :param query: Validation rules for query string parameters.
    :param form: Validation rules for form parameters.
    :param json: Validation rules for JSON parameters.
    :param headers: Request headers check rule.
    :param many: Used in conjunction with the defined JSON validation rules.
    """

    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            # Get the request object from the view function.
            request = kwargs.get("request")
            if request is None:
                raise ValueError("Request object not found")

            # Try to get the Params object
            params = getattr(request.state, "params", None)
            if not (params and isinstance(params, Params)):
                params = Params()

            # json
            if json:
                try:
                    data = await request.json()
                except pyjson.JSONDecodeError:
                    data = {}
                verified = Verify(data=data, rules=json, many=many)
                params.json = verified.params

            # query
            if query:
                verified = Verify(data=dict(request.query_params), rules=query)
                params.query = verified.params

            # form
            # !!! AssertionError: The `python-multipart` library must be installed to use form parsing.
            # >> pip install python-multipart
            if form:
                data = await request.form()
                verified = Verify(data=dict(data), rules=form)
                params.form = verified.params

            # header:
            if headers:
                verified = Verify(data=dict(request.headers), rules=headers)
                params.headers = verified.params

            # Pass the verified value using request.state
            request.state.params = params
            kwargs['request'] = request
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return inner

    return wrapper
