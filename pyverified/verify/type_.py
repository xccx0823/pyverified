import ipaddress
import re
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from email.utils import parseaddr
from typing import List as typingList, Dict as typingDict
from typing import Union, Any, Callable
from urllib.parse import urlparse

import phonenumbers

from pyverified import ValidationError, msg
from pyverified.verify._unset import Unset, unset
from pyverified.verify.base import RuleBase


@dataclass
class Bool(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

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
                    raise ValidationError(msg.message.convert.format(key=key, value=value))
            if not isinstance(value, bool):
                raise ValidationError(msg.message.type.format(key=key, value=value, type=self.get_type_name(bool)))
        return value


@dataclass
class Int(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    # gt/gte/lt/lte: Compares the value size.
    gt: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None

    # enum: enumeration.
    enum: Union[typingDict[int, Any], typingList[Union[int, float]], None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(msg.message.type.format(key=key, value=value, type=self.get_type_name(int)))

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
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    # gt/gte/lt/lte: Compares the value size.
    gt: Union[int, float, None] = None
    gte: Union[int, float, None] = None
    lt: Union[int, float, None] = None
    lte: Union[int, float, None] = None

    # digits: Reserved decimal places
    digits: Union[int, None] = None

    # decimal: Whether to convert to decimal data type
    decimal: bool = False

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            try:
                value = float(value)
            except ValueError:
                raise ValidationError(msg.message.type.format(key=key, value=value, type=self.get_type_name(float)))

            # range
            self.verify_range(key, value)

            # Reserve the specified number of decimal places.
            if self.digits is not None:
                value = round(value, self.digits)

            # Convert to decimal.
            if self.decimal:
                value = Decimal(value)

        return value


@dataclass
class Str(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    # length
    minLength: Union[int, None] = None
    maxLength: Union[int, None] = None

    # enum
    enum: Union[typingList[str], None] = None

    # pruning of the string
    # strip lstrip rstrip Functions corresponding to python string operations;
    # strip_chars lstrip_chars rstrip_chars corresponds to the parameters of
    # the above three functions.
    strip: bool = False
    lstrip: bool = False
    rstrip: bool = False
    strip_chars: Union[str, None] = None
    lstrip_chars: Union[str, None] = None
    rstrip_chars: Union[str, None] = None

    # judge
    # startswith: Determines whether the string begins with the specified
    # character or substring.
    startswith: Union[str, None] = None
    # endswith: Determines whether the string ends with the specified
    # character or substring.
    endswith: Union[str, None] = None
    # isalnum: Detects whether a string consists of letters and numbers.
    isalnum: bool = False
    # isalpha: Detects whether a string consists of only letters.
    isalpha: bool = False
    # isdecimal: Checks if the string contains only decimal characters.
    isdecimal: bool = False
    # isdigit: Detects whether a string consists only of numbers.
    isdigit: bool = False
    # isidentifier: Determines whether str is a valid identifier.
    isidentifier: bool = False
    # islower: Checks whether the letters in a string are all lowercase letters.
    islower: bool = False
    # isupper: Detects whether a string consists of all uppercase letters.
    isupper: bool = False
    # isprintable: Determine whether there is anything in the string that is not
    # visible after printing. For example: \n \t and other characters.
    isprintable: bool = False
    # isspace: Detects whether a string consists only of Spaces.
    isspace: bool = False
    # istitle: Detection Determines whether the first letter of all words in the
    # string is uppercase and other letters are lowercase. There can be other
    # characters in the string that are not letters.
    istitle: bool = False
    # include: Detects whether the string contains the specified string.
    include: Union[str, None] = None
    # exclude: Detects whether the string does not contain the specified string.
    exclude: Union[str, None] = None

    # rewriting
    # replace: replacement string content.
    # replace_args: (old, new, count)
    replace: bool = False
    replace_args: tuple = ()
    # capitalize: Change the first letter of the string to uppercase and
    # the remaining letters to lowercase.
    capitalize: bool = False
    # title: Returns a string that satisfies the title format. That is,
    # the first letter of all English words is capitalized and the other
    # English letters are lowercase.
    title: bool = False
    # swapcase: Swap both uppercase and lowercase letters in the string
    # str. Converts uppercase letters to lowercase letters and lowercase
    # letters to uppercase letters in the string str.
    swapcase: bool = False
    # lower: Converts all uppercase letters in a string to lowercase
    # letters.
    lower: bool = False
    # upper: Converts all lowercase letters in a string to uppercase
    # letters.
    upper: bool = False
    # casefold: Converts all uppercase letters in a string to lowercase
    # letters. You can also convert uppercase to lowercase in non-English
    # languages.
    casefold: bool = False

    # split: Cut the data according to the specified string, and can set
    # the conversion type of the data.
    split: Union[str, None] = None
    split2type: Any = None

    # re
    regex: Union[str, None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            # All types can be converted by str, so there is
            # no need to catch conversion failure exceptions.
            value = str(value)

            # Determine the length of the string.
            length = len(value)
            if self.minLength is not None and length < self.minLength:
                raise ValidationError(msg.message.minLength.format(key=key, value=value, minLength=self.minLength))
            if self.maxLength is not None and length > self.maxLength:
                raise ValidationError(msg.message.maxLength.format(key=key, value=value, maxLength=self.maxLength))

            # rewriting
            if self.replace:
                value = value.replace(*self.replace_args)
            if self.capitalize:
                value = value.capitalize()
            if self.title:
                value = value.title()
            if self.swapcase:
                value = value.swapcase()
            if self.lower:
                value = value.lower()
            if self.upper:
                value = value.upper()
            if self.casefold:
                value = value.casefold()

            # Remove Spaces at the beginning and end of the string.
            if self.strip:
                value = value.strip(self.strip_chars) if self.strip_chars is not None else value.strip()
            if self.lstrip:
                value = value.lstrip(self.lstrip_chars) if self.lstrip_chars is not None else value.lstrip()
            if self.rstrip:
                value = value.rstrip(self.rstrip_chars) if self.rstrip_chars is not None else value.rstrip()

            # String rule judgment.
            if self.startswith is not None and not value.startswith(self.startswith):
                raise ValidationError(msg.message.startswith.format(key=key, value=value, startswith=self.startswith))
            if self.endswith is not None and not value.endswith(self.endswith):
                raise ValidationError(msg.message.endswith.format(key=key, value=value, endswith=self.endswith))
            if self.include is not None and value not in self.include:
                raise ValidationError(msg.message.include.format(key=key, value=value, include=self.include))
            if self.exclude is not None and value in self.exclude:
                raise ValidationError(msg.message.exclude.format(key=key, value=value, exclude=self.exclude))
            if self.isalnum and not value.isalnum():
                raise ValidationError(msg.message.isalnum.format(key=key, value=value))
            if self.isalpha and not value.isalpha():
                raise ValidationError(msg.message.isalpha.format(key=key, value=value))
            if self.isdecimal and not value.isdecimal():
                raise ValidationError(msg.message.isdecimal.format(key=key, value=value))
            if self.isdigit and not value.isdigit():
                raise ValidationError(msg.message.isdigit.format(key=key, value=value))
            if self.isidentifier and not value.isidentifier():
                raise ValidationError(msg.message.isidentifier.format(key=key, value=value))
            if self.islower and not value.islower():
                raise ValidationError(msg.message.islower.format(key=key, value=value))
            if self.isupper and not value.isupper():
                raise ValidationError(msg.message.isupper.format(key=key, value=value))
            if self.isprintable and not value.isprintable():
                raise ValidationError(msg.message.isprintable.format(key=key, value=value))
            if self.isspace and not value.isspace():
                raise ValidationError(msg.message.isspace.format(key=key, value=value))
            if self.istitle and not value.istitle():
                raise ValidationError(msg.message.istitle.format(key=key, value=value))

            # split
            if self.split is not None:
                value = value.split(self.split)
                if self.split2type is not None:
                    _value = []
                    for _v in value:
                        try:
                            _v = self.split2type(_v)
                        except ValueError:
                            raise ValidationError(msg.message.type.format(
                                key=key, value=_v, type=self.get_type_name(self.split2type)))
                        _value.append(_v)
                    value = _value

            # re
            if self.regex is not None:
                if isinstance(value, list):
                    for _v in value:
                        self.verify_regex(key, _v)
                else:
                    self.verify_regex(key, value)

            # enum
            if self.enum is not None:
                if isinstance(value, list):
                    _value = []
                    for _v in value:
                        _value.append(self.verify_enum(key, _v))
                    value = _value
                else:
                    value = self.verify_enum(key, value)

        return value

    def verify_regex(self, key, value):
        if not bool(re.match(self.regex, value)):
            raise ValidationError(msg.message.regex.format(key=key, value=value, regex=self.regex))


@dataclass
class DateTime(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[datetime, date, str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    # fmt: date format.
    fmt: str = '%Y-%m-%d %H:%M:%S'

    # gt/gte/lt/lte: date size comparison.
    gt: Union[datetime, date, str, None] = None
    gte: Union[datetime, date, str, None] = None
    lt: Union[datetime, date, str, None] = None
    lte: Union[datetime, date, str, None] = None

    # enum: Date enumeration.
    enum: Union[typingList[str], typingList[datetime], typingList[date], None] = None

    def parse(self, key: str, value: Any):
        if value not in self.null_values:
            # Either date or datetime or str is converted to datetime for validation.
            try:
                value = self._try_trans_data(value)
            except ValueError:
                raise ValidationError(msg.message.type.format(
                    key=key, value=value, type=self.get_type_name(self._get_type())))

            # After the data obtained through the set fmt conversion,
            # the value is converted to the type processed internally
            value = self._try_trans_datetime(value)

            # range
            self.verify_range(key, value)

            # enum
            if self.enum is not None and value not in self.enum:
                raise ValidationError(msg.message.enum.format(key=key, value=value, enum=tuple(self.enum)))

            # Converts the result to the type defined by the current class
            if type(value) is not self._get_type():
                value = value.date()

        return value

    def execute_parse(self, key: str, value: Any):
        # Convert the data type before verifying the rule.
        self.trans_rule_value_type()
        return super().execute_parse(key, value)

    @staticmethod
    def _get_type():
        return datetime

    def trans_rule_value_type(self):
        """Converts the type of the comparison value."""

        # The conversion error does not need to return a ValidationError after
        # interception, because this is the result of the user defining the
        # error value.

        # default value
        if self.default is not unset:
            self.default = self._try_trans_datetime(self.default)

        # compare value
        if self.gt:
            self.gt = self._try_trans_datetime(self.gt)
        if self.gte:
            self.gte = self._try_trans_datetime(self.gte)
        if self.lt:
            self.lt = self._try_trans_datetime(self.lt)
        if self.lte:
            self.lte = self._try_trans_datetime(self.lte)

        # enum value
        if self.enum:
            fmt_enum = []
            for item in self.enum:
                fmt_enum.append(self._try_trans_datetime(item))
            self.enum = fmt_enum

    @staticmethod
    def _try_trans_datetime(value):
        if type(value) is date:
            value = datetime.combine(value, time())
        elif type(value) is datetime:
            pass
        else:
            # Try to parse string dates in two formats.
            # An error is reported only after both fail
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                value = datetime.strptime(value, '%Y-%m-%d')

        return value

    def _try_trans_data(self, value):
        if type(value) is date:
            value = datetime.combine(value, time())
        elif type(value) is datetime:
            pass
        else:
            value = datetime.strptime(value, self.fmt)
        return value


@dataclass
class Date(DateTime):
    fmt: str = '%Y-%m-%d'

    @staticmethod
    def _get_type():
        return date


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
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_email(value):
            raise ValidationError(msg.message.email.format(key=key, value=value))
        return value

    @staticmethod
    def is_email(e_mail: Any):
        _, email_address = parseaddr(str(e_mail))
        return '@' in email_address


@dataclass
class IPv4(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.allow_none and not self.is_ipv4(value):
            raise ValidationError(msg.message.ipv4.format(key=key, value=value))
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
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_ipv6(value):
            raise ValidationError(msg.message.ipv6.format(key=key, value=value))
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
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None
    region: str = 'CN'

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_tel(value):
            raise ValidationError(msg.message.phone.format(key=key, value=value, region=self.region))
        return value

    def is_tel(self, telephone_number: Any):
        try:
            parsed_number = phonenumbers.parse(str(telephone_number), self.region)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False


@dataclass
class Addr(RuleBase):
    # default: indicates the default value.
    # required: Whether it is required.
    # allow_none: indicates whether None is allowed.
    # multi: Check whether multiple values exist
    # func: user-defined function.
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True
    multi: bool = False
    func: Union[Callable, typingList[Callable], None] = None

    def parse(self, key: str, value: Any) -> str:
        if value not in self.null_values and not self.is_addr(value):
            raise ValidationError(msg.message.address.format(key=key, value=value))
        return value

    @staticmethod
    def is_addr(address: Any):
        try:
            parsed_url = urlparse(str(address))
            return all([parsed_url.scheme, parsed_url.netloc])
        except ValueError:
            return False
