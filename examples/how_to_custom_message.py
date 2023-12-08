from pyverify import msg
from pyverify.verify import phone


class NewMsg:
    phone = '{key}的值{value}并不是电话号码'


msg.Message.reload(NewMsg)

phone().parse('tel', '123456')
