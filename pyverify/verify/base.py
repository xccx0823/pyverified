from typing import Any

from pyverify import msg
from pyverify.exc import ValidationError
from pyverify.verify._unset import Unset, unset


class RuleBase:
    """Rule base class."""

    null_values = (unset, None, '')

    def parse(self, key: str, value: Any):
        raise NotImplementedError("parse hasn't been implemented yet.")

    def execute_parse(self, key: str, value: Any):
        if self.multi:  # noqa
            if not isinstance(value, (list, set, tuple)):
                raise ValidationError(msg.message.multi.format(key=key, value=value))
            _values = []
            for _value in value:
                _value = self.common_rules_verify(key, _value)
                _value = self.parse(key, _value)
                if self.func:  # noqa
                    _value = self.func(key, _value)  # noqa
                _values.append(_value)
            value = _values
        else:
            value = self.common_rules_verify(key, value)
            value = self.parse(key, value)
            if self.func:  # noqa
                value = self.func(key, value)  # noqa
        return value

    def verify_required(self, key: str, value: Any):
        """Check whether parameters are missing."""
        if self.required and isinstance(value, Unset):  # noqa
            raise ValidationError(msg.message.required.format(key=key, value=value))

    def verify_allow_none(self, key: str, value: Any):
        """Check whether the parameter can be None."""
        if not self.allow_none and value in self.null_values:  # noqa
            raise ValidationError(msg.message.allow_none.format(key=key, value=value))

        # When allow_none is True, value is replaced with None if it is unset.
        if isinstance(value, Unset):
            value = None

        return value

    def verify_enum(self, key, value):
        """
        There are two types of enum parameters. When the parameter is
        dict, the corresponding value is mapped. When the parameter
        is list, the parameter is checked only for whether it exists
        in the enumeration.
        """
        if isinstance(self.enum, dict):  # noqa
            try:
                value = self.enum[value]  # noqa
            except KeyError:
                raise ValidationError(msg.message.enum.format(key=key, value=value, enum=self.enum))  # noqa
        elif isinstance(self.enum, list):  # noqa
            if value not in self.enum:  # noqa
                raise ValidationError(msg.message.enum.format(key=key, value=value, enum=self.enum))  # noqa
        return value

    def verify_range(self, key: str, value: Any):
        """The range of the check value."""
        if self.gt is not None and value <= self.gt:  # noqa
            raise ValidationError(msg.message.gt.format(key=key, value=value, gt=self.gt))  # noqa
        if self.gte is not None and value < self.gte:  # noqa
            raise ValidationError(msg.message.gte.format(key=key, value=value, gte=self.gte))  # noqa
        if self.lt is not None and value >= self.lt:  # noqa
            raise ValidationError(msg.message.lt.format(key=key, value=value, lt=self.lt))  # noqa
        if self.lte is not None and value > self.lte:  # noqa
            raise ValidationError(msg.message.lte.format(key=key, value=value, lte=self.lte))  # noqa

    def set_default_value(self, value: Any):
        """Set a default value."""
        if value in self.null_values and self.default is not unset:  # noqa
            value = self.default  # noqa
        return value

    def common_rules_verify(self, key: str, value: Any):
        self.verify_required(key, value)
        value = self.verify_allow_none(key, value)
        value = self.set_default_value(value)
        return value
