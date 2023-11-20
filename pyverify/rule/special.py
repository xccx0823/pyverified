import ipaddress
from dataclasses import dataclass
from email.utils import parseaddr
from typing import Union
from urllib.parse import urlparse

import phonenumbers

from pyverify._unset import Unset, unset
from pyverify.rule.base import RuleBase


@dataclass
class Email(RuleBase):
    """
    email
    """
    default: Union[str, Unset] = unset
    required: bool = False

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

    @staticmethod
    def is_tel(phone_number: str, region: str):
        try:
            parsed_number = phonenumbers.parse(phone_number, region)
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


@dataclass
class Addr(RuleBase):
    """
    address
    """
    default: Union[str, Unset] = unset
    required: bool = False

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
