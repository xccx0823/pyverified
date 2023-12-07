from dataclasses import dataclass
from datetime import datetime, date
from typing import Union, List

from pyverify import msg
from pyverify._unset import Unset, unset
from pyverify.exc import ValidationError
from pyverify.rules.base import RuleBase


@dataclass
class Bool(RuleBase):
    """
    bool

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param convert: Whether to convert true, false The string is of Boolean type.
    """
    default: Union[bool, Unset] = unset
    required: bool = False
    allow_none: bool = True
    convert: bool = True

    def parse(self, key: str, value: Union[str, bool]) -> str:
        value = self.common_rules_verify(key, value)
        if self.convert and isinstance(value, str):
            upper_value = value.upper()
            if upper_value in 'TRUE':
                value = True
            elif upper_value == "FALSE":
                value = False
            else:
                raise ValidationError(msg.Message.convert.format(key=key, value=value))
        return value


@dataclass
class Number(RuleBase):
    """
    int/float

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param ge/gte/lt/lte: Compares the value size.
    :param enum: enumeration.
    :param digits: indicates the number of digits reserved.
    """
    default: Union[int, float, Unset] = unset
    required: bool = False
    allow_none: bool = True
    ge: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None
    enum: Union[List[Union[int, float]], None] = None
    digits: Union[int, None] = None


@dataclass
class String(RuleBase):
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


@dataclass
class DateTime(RuleBase):
    """
    datetime

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param fmt: date format.
    :param ge/gte/lt/lte: date size comparison.
    :param enum: Date enumeration.
    """
    default: Union[datetime, Unset] = unset
    required: bool = False
    allow_none: bool = True
    fmt: str = '%Y-%m-%d %H:%M:%S'
    ge: Union[datetime, str, None] = None
    gte: Union[datetime, str, None] = None
    lt: Union[datetime, str, None] = None
    lte: Union[datetime, str, None] = None
    enum: Union[List[datetime], List[str], None] = None


@dataclass
class Date(RuleBase):
    """
    date

    :param default: indicates the default value.
    :param required: Whether it is required.
    :param allow_none: indicates whether None is allowed.
    :param fmt: date format.
    :param ge/gte/lt/lte: date size comparison.
    :param enum: Date enumeration.
    """
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    fmt: str = '%Y-%m-%d'
    ge: Union[date, str, None] = None
    gte: Union[date, str, None] = None
    lt: Union[date, str, None] = None
    lte: Union[date, str, None] = None
    enum: Union[List[date], List[str], None] = None


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


char = String
num = Number
bol = Bool
dtime = DateTime
dt = Date
dic = Dict
lis = List
