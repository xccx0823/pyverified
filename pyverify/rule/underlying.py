from dataclasses import dataclass
from datetime import datetime, date
from typing import Union, List

from pyverify._unset import Unset, unset
from pyverify.rule.base import RuleBase


@dataclass
class Bool(RuleBase):
    """
    bool

    python内置数据类型

    :param default: 默认值
    :param required: 是否是必须的
    :param allow_none: 是否允许为None
    :param convert: 是否转变 ture，false 这种字符串为布尔类型
    """
    default: Union[bool, Unset] = unset
    required: bool = False
    allow_none: bool = True
    convert: bool = True


@dataclass
class Number(RuleBase):
    """
    int/float

    python内置数据类型

    :param default: 默认值
    :param required: 是否是必须的
    :param allow_none: 是否允许为None
    :param ge/gte/lt/lte: 数值大小比较
    :param enum: 枚举
    :param digits: 保留小数位数
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

    python内置数据类型

    :param default: 默认值
    :param required: 是否是必须的
    :param allow_none: 是否允许为None
    :param minLength/maxLength: 字符串长度限制
    :param regex: 字符串正则规则匹配
    :param enum: 枚举
    :param trim: 去除字符串左右两边空格
    :param split: 按照指定字符或字符串切割字符串
    :param startswith: 字符串必须以指定字符或字符串开头
    :param endswith: 字符串必须以指定字符或字符串结尾
    :param unStartswith: 字符串不能以指定字符或字符串结尾
    :param unEndswith: 字符串不能以指定字符或字符串结尾
    :param include: 字符串必须包含指定字符或字符串
    :param exclude: 字符串必须不包含指定字符或字符串
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

    python日期模块数据类型

    :param default: 默认值
    :param required: 是否是必须的
    :param allow_none: 是否允许为None
    :param fmt: 日期格式
    :param ge/gte/lt/lte: 日期大小比较
    :param enum: 日期枚举
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

    python日期模块数据类型

    :param default: 默认值
    :param required: 是否是必须的
    :param allow_none: 是否允许为None
    :param fmt: 日期格式
    :param ge/gte/lt/lte: 日期大小比较
    :param enum: 日期枚举
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
class Flat(RuleBase):
    """
    dict/list

    嵌套结构

    :param required: 是否是必须的
    :param allow_none: 是否允许为None
    :param subset: 子规则结构
    :param multi: 当为True时表示验证数据为列表嵌套字典，当为False时是单个字典
    """
    subset: dict
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False


char = String
num = Number
bol = Bool
dtime = DateTime
dt = Date
flat = Flat
