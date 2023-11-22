from pyverify import msg
from pyverify.rules.special import Tel


class NewMsg:
    telephone = '{key}的值{value}并不是电话号码'


msg.VerifyMessage.reload(NewMsg)

Tel().parse('tel', '123456')
