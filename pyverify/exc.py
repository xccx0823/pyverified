class ValidationError(Exception):
    """Rule check failure exception class."""

    def __init__(self, msg: str):
        self.msg = msg
