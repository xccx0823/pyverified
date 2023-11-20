import ipaddress
from dataclasses import dataclass
from typing import Union

from pyverify._unset import Unset, unset
from pyverify.rule.base import RuleBase

EMAIL_REGEX = ''
IPV4_REGEX = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
IPV6_REGEX = ''
TEL_REGEX = ''
ADDR_REGEX = ''


@dataclass
class Email(RuleBase):
    """
    email
    """
    default: Union[str, Unset] = unset
    required: bool = False


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


email = Email
ipv4 = IPv4
ipv6 = IPv6
tel = Tel
js = Json
addr = Addr
