import ipaddress
from dataclasses import dataclass
from datetime import datetime, date
from email.utils import parseaddr
from typing import List, Dict as typingDict
from typing import Union, Any, Callable
from urllib.parse import urlparse

import phonenumbers

from pyverify import msg
from pyverify.exc import ValidationError
from pyverify.verify._unset import Unset, unset
from pyverify.verify.base import RuleBase


@dataclass
class Bool(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # func: user-defined function.
    default: Union[bool, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    # convert: Whether to convert true, false The string is of Boolean type.
    convert: bool = True

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
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # func: user-defined function.
    default: Union[int, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    # gt/gte/lt/lte: Compares the value size.
    gt: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None

    # enum: enumeration.
    enum: Union[typingDict[int, Any], List[Union[int, float]], None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(msg.Message.typeInt.format(key=key, value=value))

            # range
            self.verify_range(key, value)

        # enum
        value = self.verify_enum(key, value)

        return value


@dataclass
class Float(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # func: user-defined function.
    default: Union[int, float, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    # gt/gte/lt/lte: Compares the value size.
    gt: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None

    # digits: Reserved decimal places
    digits: Union[int, None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
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
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True

    # Length
    minLength: Union[int, None] = None
    maxLength: Union[int, None] = None

    # Enum
    enum: Union[List[str], None] = None

    # Pruning of the string
    # strip lstrip rstrip Functions corresponding to python string operations;
    # strip_chars lstrip_chars rstrip_chars corresponds to the parameters of the above three functions.
    strip: bool = False
    lstrip: bool = False
    rstrip: bool = False
    strip_chars: Union[str, None] = None
    lstrip_chars: Union[str, None] = None
    rstrip_chars: Union[str, None] = None

    regex: Union[str, None] = None
    startswith: Union[str, None] = None
    endswith: Union[str, None] = None
    unStartswith: Union[str, None] = None
    unEndswith: Union[str, None] = None
    include: Union[str, None] = None
    exclude: Union[str, None] = None
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            # All types can be converted by str, so there is
            # no need to catch conversion failure exceptions.
            value = str(value)

            # Determine the length of the string.
            length = len(value)
            if self.minLength is not None and length < self.minLength:
                raise
            if self.maxLength is not None and length > self.maxLength:
                raise

            # Remove Spaces at the beginning and end of the string.
            if self.strip:
                value = value.strip(self.strip_chars) if self.strip_chars is not None else value.strip()
            if self.lstrip:
                value = value.lstrip(self.lstrip_chars) if self.lstrip_chars is not None else value.lstrip()
            if self.rstrip:
                value = value.rstrip(self.rstrip_chars) if self.rstrip_chars is not None else value.rstrip()

        # enum
        value = self.verify_enum(key, value)

        return value


@dataclass
class DateTime(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # func: user-defined function.
    default: Union[datetime, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    # fmt: date format.
    fmt: str = '%Y-%m-%d %H:%M:%S'

    # gt/gte/lt/lte: date size comparison.
    gt: Union[datetime, str, None] = None
    gte: Union[datetime, str, None] = None
    lt: Union[datetime, str, None] = None
    lte: Union[datetime, str, None] = None

    # enum: Date enumeration.
    enum: Union[List[datetime], List[str], None] = None

    def parse(self, key: str, value: Any):
        pass


@dataclass
class Date(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # func: user-defined function.
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    # fmt: date format.
    fmt: str = '%Y-%m-%d'

    # gt/gte/lt/lte: date size comparison.
    gt: Union[date, str, None] = None
    gte: Union[date, str, None] = None
    lt: Union[date, str, None] = None
    lte: Union[date, str, None] = None

    # enum: Date enumeration.
    enum: Union[List[date], List[str], None] = None

    def parse(self, key: str, value: Any):
        pass


@dataclass
class Dict(RuleBase):
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # subset: rule structure.
    # multi: When True, the validation data is a list nested dictionary, when False, a single dictionary.
    subset: dict
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False

    # dest: indicates that all information about a subordinate structure is obtained without verification.
    dest: bool = False


@dataclass
class List(RuleBase):
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # subset: rule structure.
    # multi: When True, the validation data is a list nested dictionary, when False, a single dictionary.
    subset: dict
    default: Union[date, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = True

    # dest: indicates that all information about a subordinate structure is obtained without verification.
    dest: bool = False


@dataclass
class Email(RuleBase):
    """
    email
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_email(value):
            raise ValidationError(msg.Message.email.format(key=key, value=value))
        return value

    @staticmethod
    def is_email(e_mail: Any):
        _, email_address = parseaddr(str(e_mail))
        return '@' in email_address


@dataclass
class IPv4(RuleBase):
    """
    ipv4
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.allow_none and not self.is_ipv4(value):
            raise ValidationError(msg.Message.ipv4.format(key=key, value=value))
        return value

    @staticmethod
    def is_ipv4(address: Any) -> bool:
        try:
            ipaddress.IPv4Address(str(address))
            return True
        except ipaddress.AddressValueError:
            return False


@dataclass
class IPv6(RuleBase):
    """
    ipv6
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_ipv6(value):
            raise ValidationError(msg.Message.ipv6.format(key=key, value=value))
        return value

    @staticmethod
    def is_ipv6(address: Any) -> bool:
        try:
            ipaddress.IPv6Address(str(address))
            return True
        except ipaddress.AddressValueError:
            return False


@dataclass
class Phone(RuleBase):
    """
    phone
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    region: str = 'CN'
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_tel(value):
            raise ValidationError(msg.Message.phone.format(key=key, value=value, region=self.region))
        return value

    def is_tel(self, telephone_number: Any):
        try:
            parsed_number = phonenumbers.parse(str(telephone_number), self.region)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False


@dataclass
class Addr(RuleBase):
    """
    address
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    func: Union[Callable, None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_addr(value):
            raise ValidationError(msg.Message.address.format(key=key, value=value))
        return value

    @staticmethod
    def is_addr(address: Any):
        try:
            parsed_url = urlparse(str(address))
            return all([parsed_url.scheme, parsed_url.netloc])
        except ValueError:
            return False


email = Email
ipv4 = IPv4
ipv6 = IPv6
phone = Phone
addr = Addr
