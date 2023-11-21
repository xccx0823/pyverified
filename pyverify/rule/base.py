from typing import Any


class RuleBase:
    """规则类型基类"""

    def parse(self, key: str, value: Any):
        raise NotImplementedError("parse hasn't been implemented yet.")
