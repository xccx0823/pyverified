from typing import Any

from pyverify import msg
from pyverify.exc import ValidationError
from pyverify.verify._unset import Unset, unset


class RuleBase:
    """Rule base class."""

    def parse(self, key: str, value: Any):
        raise NotImplementedError("parse hasn't been implemented yet.")

    def verify_required(self, key: str, value: Any):
        """Check whether parameters are missing."""
        if self.required and isinstance(value, Unset):  # noqa
            raise ValidationError(msg.Message.required.format(key=key, value=value))

    def verify_allow_none(self, key: str, value: Any):
        """Check whether the parameter can be None."""
        if not self.allow_none and value in (None, unset, ''):  # noqa
            raise ValidationError(msg.Message.allow_none.format(key=key, value=value))

        # When allow_none is True, value is replaced with None if it is unset.
        if isinstance(value, Unset):
            value = None

        return value

    def set_default_value(self, value: Any):
        """Set a default value."""
        if value in (unset, None, '') and self.default is not unset:  # noqa
            value = self.default  # noqa
        return value

    def common_rules_verify(self, key: str, value: Any):
        self.verify_required(key, value)
        value = self.verify_allow_none(key, value)
        value = self.set_default_value(value)
        return value
