from typing import Any

from pyverify import msg
from pyverify._unset import Unset, unset
from pyverify.exc import ValidationError


class RuleBase:
    """规则类型基类"""

    def parse(self, key: str, value: Any):
        raise NotImplementedError("parse hasn't been implemented yet.")

    def verify_required(self, key: str, value: Any):
        """校验参数是否有缺失"""
        if self.required and isinstance(value, Unset):  # noqa
            raise ValidationError(msg.VerifyMessage.required.format(key=key, value=value))

    def verify_allow_none(self, key: str, value: Any):
        """校验参数是否可以为None"""
        if not self.allow_none and value in (None, unset):  # noqa
            raise ValidationError(msg.VerifyMessage.allow_none.format(key=key, value=value))

        # 当allow_none为True时，value如果时unset，则替换为None
        if isinstance(value, Unset):
            value = None

        return value

    def set_default_value(self, value: Any):
        """设置默认值"""
        if isinstance(value, Unset) and self.default is not None:  # noqa
            value = self.default  # noqa
        return value

    def common_rules_verify(self, key: str, value: Any):
        self.verify_required(key, value)
        value = self.verify_allow_none(key, value)
        value = self.set_default_value(value)
        return value
