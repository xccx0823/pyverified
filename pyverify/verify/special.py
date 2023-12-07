import ipaddress
from dataclasses import dataclass
from email.utils import parseaddr
from typing import Union, Any
from urllib.parse import urlparse

import phonenumbers

from pyverify import msg
from pyverify.exc import ValidationError
from pyverify.verify._unset import Unset, unset
from pyverify.verify.base import RuleBase


@dataclass
class Email(RuleBase):
    """
    email
    """
    default: Union[str, Unset] = unset
    required: bool = False
    allow_none: bool = True

    def parse(self, key: str, value: Any) -> str:
        value = self.common_rules_verify(key, value)
        if value and not self.is_email(value):
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

    def parse(self, key: str, value: Any) -> str:
        value = self.common_rules_verify(key, value)
        if value and not self.allow_none and not self.is_ipv4(value):
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

    def parse(self, key: str, value: Any) -> str:
        value = self.common_rules_verify(key, value)
        if value and not self.is_ipv6(value):
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

    def parse(self, key: str, value: Any) -> str:
        value = self.common_rules_verify(key, value)
        if value and not self.is_tel(value):
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

    def parse(self, key: str, value: Any) -> str:
        value = self.common_rules_verify(key, value)
        if value and not self.is_addr(value):
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
