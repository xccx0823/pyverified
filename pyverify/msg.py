class VerifyMessage:
    """校验异常信息"""
    email = '当前字符串并不是邮箱'
    telephone = '当前字符串并不是电话号码'
    ipv4 = '当前字符串并不是ipv4地址'
    ipv6 = '当前字符串并不是ipv6地址'
    address = '当前字符串并不是链接地址'

    @classmethod
    def reload(cls, clss):
        msgs = dict(filter(lambda x: not x[0].startswith('__'), vars(clss).items()))
        for key, msg in msgs.items():
            setattr(cls, key, msg)
