from datetime import date, datetime

from pyverify.verify.special import email, ipv4, ipv6, phone, addr
from pyverify.verify.underlying import Str, Num, Bool, DateTime, Date, Dict, List

TYPE_MAPPING: dict = {
    str: Str,
    int: Num,
    float: Num,
    bool: Bool,
    dict: Dict,
    list: List,
    date: Date,
    datetime: DateTime,
    email: email,
    ipv4: ipv4,
    ipv6: ipv6,
    phone: phone,
    addr: addr
}


def rule(t, **kwargs):
    if t in TYPE_MAPPING:
        return TYPE_MAPPING[t](**kwargs)
    else:
        raise TypeError(f"The type of the rule is not defined: {t}.")
