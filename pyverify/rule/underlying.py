from dataclasses import dataclass
from datetime import datetime, date
from typing import Union, List

from pyverify._unset import Unset, unset
from pyverify.rule.base import RuleBase


@dataclass
class Bool(RuleBase):
    """
    bool
    """
    default: Union[bool, Unset] = unset
    required: bool = False
    raiseValue: bool = True


@dataclass
class Number(RuleBase):
    """
    int/float
    """
    default: Union[int, float, Unset] = unset
    required: bool = False
    ge: Union[int, None] = None
    gte: Union[int, None] = None
    lt: Union[int, None] = None
    lte: Union[int, None] = None
    enum: Union[List[Union[int, float]], None] = None
    digits: Union[int, None] = None
    dest: bool = False


@dataclass
class String(RuleBase):
    """
    str
    """
    default: Union[str, Unset] = unset
    required: bool = False
    minLength: Union[int, None] = None
    maxLength: Union[int, None] = None
    regex: Union[str, None] = None
    enum: Union[List[str], None] = None
    dest: bool = False
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
    """
    default: Union[datetime, Unset] = unset
    required: bool = False
    fmt: str = '%Y-%m-%d %H:%M:%S'
    ge: Union[datetime, None] = None
    gte: Union[datetime, None] = None
    lt: Union[datetime, None] = None
    lte: Union[datetime, None] = None
    enum: Union[List[datetime], None] = None
    dest: bool = False


@dataclass
class Date(RuleBase):
    """
    date
    """
    default: Union[date, Unset] = unset
    required: bool = False
    fmt: str = '%Y-%m-%d'
    ge: Union[date, None] = None
    gte: Union[date, None] = None
    lt: Union[date, None] = None
    lte: Union[date, None] = None
    enum: Union[List[date], None] = None
    dest: bool = False


@dataclass
class Flat(RuleBase):
    """
    dict/list
    """
    subset: dict
    multi: bool = False


char = String
num = Number
bol = Bool
dtime = DateTime
dt = Date
flat = Flat
