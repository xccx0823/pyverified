from datetime import date, datetime
from typing import Dict, Any, Callable

from pyverify.rule.special import email, ipv4, ipv6, tel, js, addr
from pyverify.rule.underlying import char, num, bol, dtime, dt, flat

TYPE_MAPPING: Dict[Any, Callable] = {
    str: char,
    int: num,
    float: num,
    bool: bol,
    date: dt,
    datetime: dtime,
    dict: flat
}


def f(t, **kwargs):
    """定义方式的一种，让每行变的精简一点"""
    if t in TYPE_MAPPING:
        return TYPE_MAPPING[t](**kwargs)
    elif t == 'email':
        return email(**kwargs)
    elif t == 'ipv4':
        return ipv4(**kwargs)
    elif t == 'ipv6':
        return ipv6(**kwargs)
    elif t == 'telephone':
        return tel(**kwargs)
    elif t == 'addr':
        return addr(**kwargs)
    else:
        raise TypeError(f"The type of the rule is not defined: {t}")
