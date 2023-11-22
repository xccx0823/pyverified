class Unset:
    """Unset value."""

    def __bool__(self):
        return False


unset = Unset()
