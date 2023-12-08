from datetime import date, datetime

from pyverify.verify.type_ import Str, Int, Float, Bool, DateTime, Date, Dict, List, email, ipv4, ipv6, phone, addr

TYPE_MAPPING: dict = {
    str: Str,
    int: Int,
    float: Float,
    bool: Bool,
    dict: Dict,
    list: List,
    date: Date,
    datetime: DateTime,
    email: email,
    ipv4: ipv4,
    ipv6: ipv6,
    phone: phone,
    addr: addr,
    'str': Str,
    'int': Int,
    'float': Float,
    'bool': Bool,
    'dict': Dict,
    'list': List,
    'date': Date,
    'datetime': DateTime,
    'email': email,
    'ipv4': ipv4,
    'ipv6': ipv6,
    'phone': phone,
    'addr': addr
}


def rule(t, **kwargs):
    if t in TYPE_MAPPING:
        return TYPE_MAPPING[t](**kwargs)
    else:
        raise TypeError(f"The type of the rule is not defined: {t}.")
