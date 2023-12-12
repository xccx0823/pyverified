from pyverified.exc import ValidationError
from pyverified.msg import message
from pyverified.verify.type_ import Str, Int, Float, Bool, DateTime, Date, Dict, List, Email, IPv4, IPv6, Phone, Addr
from pyverified.verify.verify import Verify


class rule:  # noqa
    """Easy and neat to use."""
    str = Str
    int = Int
    float = Float
    bool = Bool
    dict = Dict
    list = List
    date = Date
    datetime = DateTime
    email = Email
    ipv4 = IPv4
    ipv6 = IPv6
    phone = Phone
    addr = Addr
