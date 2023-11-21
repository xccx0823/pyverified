import ipaddress
import json
from dataclasses import dataclass
from email.utils import parseaddr
from typing import Union
from urllib.parse import urlparse

import phonenumbers

from pyverify import msg
from pyverify._unset import Unset, unset
from pyverify.exc import ValidationError
from pyverify.rule.base import RuleBase


@dataclass
class Email(RuleBase):
    """
    email
    """
    default: Union[str, Unset] = unset
    required: bool = False

    def parse(self, key: str, value: str) -> str:
        if not self.is_email(value):
            raise ValidationError(msg.VerifyMessage.email.format(key=key, value=value))
        return value

    @staticmethod
    def is_email(e_mail: str):
        _, email_address = parseaddr(e_mail)
        return '@' in email_address


@dataclass
class IPv4(RuleBase):
    """
    ipv4
    """
    default: Union[str, Unset] = unset
    required: bool = False

    def parse(self, key: str, value: str) -> str:
        if not self.is_ipv4(value):
            raise ValidationError(msg.VerifyMessage.ipv4.format(key=key, value=value))
        return value

    @staticmethod
    def is_ipv4(address: str) -> bool:
        try:
            ipaddress.IPv4Address(address)
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

    def parse(self, key: str, value: str) -> str:
        if not self.is_ipv6(value):
            raise ValidationError(msg.VerifyMessage.ipv6.format(key=key, value=value))
        return value

    @staticmethod
    def is_ipv6(address: str) -> bool:
        try:
            ipaddress.IPv6Address(address)
            return True
        except ipaddress.AddressValueError:
            return False


@dataclass
class Tel(RuleBase):
    """
    telephone
    """
    default: Union[str, Unset] = unset
    required: bool = False
    region: str = 'CN'

    def parse(self, key: str, value: str) -> str:
        if not self.is_tel(value):
            raise ValidationError(msg.VerifyMessage.telephone.format(key=key, value=value, region=self.region))
        return value

    def is_tel(self, telephone_number: str):
        try:
            parsed_number = phonenumbers.parse(telephone_number, self.region)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False


@dataclass
class Json(RuleBase):
    """
    json
    """
    default: Union[str, Unset] = unset
    required: bool = False
    cls = None

    def json_loads(self, json_string):
        json.loads(json_string, cls=self.cls)


@dataclass
class Addr(RuleBase):
    """
    address
    """
    default: Union[str, Unset] = unset
    required: bool = False

    def parse(self, key: str, value: str) -> str:
        if not self.is_addr(value):
            raise ValidationError(msg.VerifyMessage.address.format(key=key, value=value))
        return value

    @staticmethod
    def is_addr(address):
        try:
            parsed_url = urlparse(address)
            return all([parsed_url.scheme, parsed_url.netloc])
        except ValueError:
            return False


email = Email
ipv4 = IPv4
ipv6 = IPv6
tel = Tel
js = Json
addr = Addr
