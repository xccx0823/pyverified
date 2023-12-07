from pyverify import msg
from pyverify.verify.special import Phone


class NewMsg:
    phone = '{key}的值{value}并不是电话号码'


msg.Message.reload(NewMsg)

Phone().parse('tel', '123456')
