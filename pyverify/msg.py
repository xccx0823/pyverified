class Message:
    """Define check exception information."""
    # special type
    email = '{key}不是邮箱格式。'
    phone = '{key}不是电话号码格式。'
    ipv4 = '{key}不是ipv4地址格式。'
    ipv6 = '{key}不是ipv6地址格式。'
    address = '{key}不是链接地址格式。'

    # common
    required = '{key}是必须的。'
    allow_none = '{key}不能为空。'
    many = '校验数据必须是数组。'
    multi = '{key}必须是数组。'
    enum = '{key}的值{value}不在{enum}中。'
    gt = '{key}的值{value}必须大于{gt}。'
    gte = '{key}的值{value}必须大于等于{gte}。'
    lt = '{key}的值{value}必须小于{lt}。'
    lte = '{key}的值{value}必须小于等于{lte}。'

    # flask
    params = '视图函数{func}的请求参数必须是字典。'

    # type
    typeInt = '{key}的值{value}不是数值类型。'
    typeFloat = '{key}的值{value}不是浮点类型。'

    # bool
    typeBool = '{key}的值{value}不是布尔类型。'
    convert = '{key}的值{value}不能转化为布尔类型。'

    # str
    minLength = '{key}的值{value}的长度不能小于{minLength}。'
    maxLength = '{key}的值{value}的长度不能大于{maxLength}。'
    startswith = '{key}的值{value}必须以{startswith}字符串开头。'
    endswith = '{key}的值{value}必须以{endswith}字符串结尾。'
    include = '{key}的值{value}中必须包括{include}字符串。'
    exclude = '{key}的值{value}中不能包括{exclude}字符串。'
    isalnum = '{key}的值{value}必须由字母和数字组成。'
    isalpha = '{key}的值{value}必须由字母组成。'
    isdecimal = '{key}的值{value}必须由十进制数字组成。'
    isdigit = '{key}的值{value}必须由数字组成。'
    isidentifier = '{key}的值{value}必须是合法的标识符。'
    islower = '{key}的值{value}字母部分必须全是小写。'
    isupper = '{key}的值{value}字母部分必须全是大写。'
    isprintable = '{key}的值{value}不可以全部打印。'
    isspace = '{key}的值{value}必须由空白字符组成。'
    istitle = '{key}的值{value}必须是标题化的。'

    @classmethod
    def reload(cls, clss):
        msgs = dict(filter(lambda x: not x[0].startswith('__'), vars(clss).items()))
        for key, msg in msgs.items():
            setattr(cls, key, msg)
