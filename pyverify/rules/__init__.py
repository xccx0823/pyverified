from datetime import date, datetime
from typing import Dict, Any, Callable

from pyverify.rules.special import email, ipv4, ipv6, tel, addr
from pyverify.rules.underlying import char, num, bol, dtime, dt, dic, lis

TYPE_MAPPING: Dict[Any, Callable] = {
    str: char,
    int: num,
    float: num,
    bool: bol,
    dict: dic,
    list: lis,
    date: dt,
    datetime: dtime,
    email: email,
    ipv4: ipv4,
    ipv6: ipv6,
    tel: tel,
    addr: addr,
}


def rule(t, **kwargs):
    if t in TYPE_MAPPING:
        return TYPE_MAPPING[t](**kwargs)
    else:
        raise TypeError(f"The type of the rule is not defined: {t}.")
