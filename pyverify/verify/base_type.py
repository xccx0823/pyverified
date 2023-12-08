from dataclasses import dataclass
from datetime import datetime, date
from typing import Union, List, Any, Dict as typingDict, Callable

from pyverify import msg
from pyverify.exc import ValidationError
from pyverify.verify._unset import Unset, unset
from pyverify.verify.base import RuleBase


@dataclass
class Bool(RuleBase):
    """
    bool

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param convert: Whether to convert true, false The string is of Boolean type.
    :param func: user-defined function.
    """
    default: Union[bool, Unset] = unset
    required: bool = False
    allow_none: bool = True
    convert: bool = True
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any) -> bool:
        if value not in self.null_values:
            if self.convert and isinstance(value, str):
                upper_value = value.upper()
                if upper_value == 'TRUE':
                    value = True
                elif upper_value == "FALSE":
                    value = False
                else:
                    raise ValidationError(msg.Message.convert.format(key=key, value=value))
            if not isinstance(value, bool):
                raise ValidationError(msg.Message.typeBool.format(key=key, value=value))
        return value


@dataclass
class Int(RuleBase):
    """
    int

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param gt/gte/lt/lte: Compares the value size.
    :param enum: enumeration.
    :param func: user-defined function.
    """
    default: Union[int, Unset] = unset
    required: bool = False
    allow_none: bool = True
    gt: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None
    enum: Union[typingDict[int, Any], List[Union[int, float]], None] = None
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            # Attempts to convert the value to type int, intercepts
            # ValueError and returns ValidationError.
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(msg.Message.typeInt.format(key=key, value=value))

            # range
            self.verify_range(key, value)

        # There are two types of enum parameters. When the parameter is
        # dict, the corresponding value is mapped. When the parameter
        # is list, the parameter is checked only for whether it exists
        # in the enumeration.
        if isinstance(self.enum, dict):
            try:
                value = self.enum[value]
            except KeyError:
                raise ValidationError(msg.Message.enum.format(key=key, value=value, enum=self.enum))
        elif isinstance(self.enum, list):
            if value not in self.enum:
                raise ValidationError(msg.Message.enum.format(key=key, value=value, enum=self.enum))

        return value


@dataclass
class Float(RuleBase):
    """
    float

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param gt/gte/lt/lte: Compares the value size.
    :param func: user-defined function.
    """
    default: Union[int, float, Unset] = unset
    required: bool = False
    allow_none: bool = True
    gt: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None
    digits: Union[int, None] = None
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            # Attempts to convert the value to type int, intercepts
            # ValueError and returns ValidationError.
            try:
                value = float(value)
            except ValueError:
                raise ValidationError(msg.Message.typeFloat.format(key=key, value=value))

            # range
            self.verify_range(key, value)

        # Reserve the specified number of decimal places.
        if self.digits is not None:
            value = round(value, self.digits)

        return value


@dataclass
class Str(RuleBase):
    """
    str

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param minLength/maxLength: indicates the string length limit.
    :param regex: matches the string regular rule.
    :param enum: enumeration.
    :param trim: Removes the Spaces on the left and right sides of the string.
    :param split: Split the string according to the specified character or string.
    :param startswith: The string must start with the specified character or string.
    :param endswith: The string must end with the specified character or string.
    :param unStartswith: The string cannot end with a specified character or string.
    :param unEndswith: The string cannot end with a specified character or string.
    :param include: The string must contain the specified character or string.
    :param exclude: The character string must exclude the specified character or string.
    :param func: user-defined function.
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    minLength: Union[int, None] = None
    maxLength: Union[int, None] = None
    regex: Union[str, None] = None
    enum: Union[List[str], None] = None
    trim: bool = False
    split: Union[str, None] = None
    startswith: Union[str, None] = None
    endswith: Union[str, None] = None
    unStartswith: Union[str, None] = None
    unEndswith: Union[str, None] = None
    include: Union[str, None] = None
    exclude: Union[str, None] = None
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any):
        pass


@dataclass
class DateTime(RuleBase):
    """
    datetime

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param fmt: date format.
    :param gt/gte/lt/lte: date size comparison.
    :param enum: Date enumeration.
    :param func: user-defined function.
    """
    default: Union[datetime, Unset] = unset
    required: bool = False
    allow_none: bool = True
    fmt: str = '%Y-%m-%d %H:%M:%S'
    gt: Union[datetime, str, None] = None
    gte: Union[datetime, str, None] = None
    lt: Union[datetime, str, None] = None
    lte: Union[datetime, str, None] = None
    enum: Union[List[datetime], List[str], None] = None
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any):
        pass


@dataclass
class Date(RuleBase):
    """
    date

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param fmt: date format.
    :param gt/gte/lt/lte: date size comparison.
    :param enum: Date enumeration.
    :param func: user-defined function.
    """
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    fmt: str = '%Y-%m-%d'
    gt: Union[date, str, None] = None
    gte: Union[date, str, None] = None
    lt: Union[date, str, None] = None
    lte: Union[date, str, None] = None
    enum: Union[List[date], List[str], None] = None
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any):
        pass


@dataclass
class Dict(RuleBase):
    """
    dict

    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param subset: rule structure.
    :param multi: When True, the validation data is a list nested dictionary, when False, a single dictionary.
    :param dest: indicates that all information about a subordinate structure is obtained without verification.
    """
    subset: dict
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    dest: bool = False


@dataclass
class List(RuleBase):
    """
    list

    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param subset: rule structure.
    :param multi: When True, the validation data is a list nested dictionary, when False, a single dictionary.
    :param dest: indicates that all information about a subordinate structure is obtained without verification.
    """
    subset: dict
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = True
    dest: bool = False
