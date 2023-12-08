from pyverify import msg, rule


class NewMsg:
    phone = '{key}的值{value}并不是电话号码'


msg.Message.reload(NewMsg)

rule.phone().parse('tel', '123456')
