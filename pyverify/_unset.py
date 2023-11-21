class Unset:
    """未设置的值"""

    def __bool__(self):
        return False


unset = Unset()
