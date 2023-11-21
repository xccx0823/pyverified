class VerifyMessage:
    """校验异常信息"""
    email = '当前参数字符串并不是邮箱'
    telephone = '当前参数字符串并不是电话号码'
    ipv4 = '当前参数字符串并不是ipv4地址'
    ipv6 = '当前参数字符串并不是ipv6地址'
    address = '当前参数字符串并不是链接地址'

    required = '当前参数是必须的'
    allow_none = '当前参数不能为None'

    @classmethod
    def reload(cls, clss):
        msgs = dict(filter(lambda x: not x[0].startswith('__'), vars(clss).items()))
        for key, msg in msgs.items():
            setattr(cls, key, msg)
