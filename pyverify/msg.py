class _Message:
    """Define check exception information."""
    # special type
    email = '`{key}` 的值 `{value}` 不是邮箱格式。'
    phone = '`{key}` 的值 `{value}` 不是电话号码格式。'
    ipv4 = '`{key}` 的值 `{value}` 不是ipv4地址格式。'
    ipv6 = '`{key}` 的值 `{value}` 不是ipv6地址格式。'
    address = '`{key}` 的值 `{value}` 不是链接地址格式。'

    # common
    required = '`{key}` 是必须的。'
    allow_none = '`{key}` 不能为空。'
    many = '校验数据必须是数组。'
    multi = '`{key}` 必须是数组。'
    enum = '`{key}` 的值 `{value}` 不在 `{enum}` 中。'
    gt = '`{key}` 的值 `{value}` 必须大于 `{gt}` 。'
    gte = '`{key}` 的值 `{value}` 必须大于等于 `{gte}` 。'
    lt = '`{key}` 的值 `{value}` 必须小于 `{lt}` 。'
    lte = '`{key}` 的值 `{value}` 必须小于等于 `{lte}` 。'

    # type
    type = '`{key}` 的值 `{value}` 无法转化为 `{type}` 类型。'

    # bool
    convert = '`{key}` 的值 `{value}` 不能转化为布尔类型。'

    # str
    minLength = '`{key}` 的值 `{value}` 的长度不能小于 `{minLength}`。'
    maxLength = '`{key}` 的值 `{value}` 的长度不能大于 `{maxLength}`。'
    startswith = '`{key}` 的值 `{value}` 必须以 `{startswith}` 字符串开头。'
    endswith = '`{key}` 的值 `{value}` 必须以 `{endswith}` 字符串结尾。'
    include = '`{key}` 的值 `{value}` 中必须包括 `{include}` 字符串。'
    exclude = '`{key}` 的值 `{value}` 中不能包括 `{exclude}` 字符串。'
    isalnum = '`{key}` 的值 `{value}` 必须由字母和数字组成。'
    isalpha = '`{key}` 的值 `{value}` 必须由字母组成。'
    isdecimal = '`{key}` 的值 `{value}` 必须由十进制数字组成。'
    isdigit = '`{key}` 的值 `{value}` 必须由数字组成。'
    isidentifier = '`{key}` 的值 `{value}` 必须是合法的标识符。'
    islower = '`{key}` 的值 `{value}` 字母部分必须全是小写。'
    isupper = '`{key}` 的值 `{value}` 字母部分必须全是大写。'
    isprintable = '`{key}` 的值 `{value}` 不可以全部打印。'
    isspace = '`{key}` 的值 `{value}` 必须由空白字符组成。'
    istitle = '`{key}` 的值 `{value}` 必须是标题化的。'
    regex = '`{key}` 的值 `{value}` 不满足正则规则 `{regex}`。'

    @classmethod
    def reload(cls, clss):
        msgs = dict(filter(lambda x: not x[0].startswith('__'), vars(clss).items()))
        for key, msg in msgs.items():
            setattr(cls, key, msg)

    @classmethod
    def english(cls):
        cls.reload(_MessageEn)


message = _Message


class _MessageEn:
    """Define check exception information."""
    # special type
    email = 'The value `{value}` for `{key}` is not in email format.'
    phone = 'The value `{value}` for `{key}` is not in phone number format.'
    ipv4 = 'The value `{value}` for `{key}` is not in IPv4 address format.'
    ipv6 = 'The value `{value}` for `{key}` is not in IPv6 address format.'
    address = 'The value `{value}` for `{key}` is not in URL address format.'

    # common
    required = '`{key}` is required.'
    allow_none = '`{key}` cannot be empty.'
    many = 'Validation data must be an array.'
    multi = '`{key}` must be an array.'
    enum = 'The value `{value}` of `{key}` is not in the allowed values: `{enum}`.'
    gt = 'The value `{value}` of `{key}` must be greater than `{gt}`.'
    gte = 'The value `{value}` of `{key}` must be greater than or equal to `{gte}`.'
    lt = 'The value `{value}` of `{key}` must be less than `{lt}`.'
    lte = 'The value `{value}` of `{key}` must be less than or equal to `{lte}`.'
    type = 'The value `{value}` of `{key}` cannot be converted to type `{type}`'

    # bool
    convert = 'The value `{value}` of `{key}` cannot be converted to boolean type.'

    # str
    minLength = 'The length of `{value}` for `{key}` must not be less than `{minLength}`.'
    maxLength = 'The length of `{value}` for `{key}` must not exceed `{maxLength}`.'
    startswith = 'The value `{value}` for `{key}` must start with the string `{startswith}`.'
    endswith = 'The value `{value}` for `{key}` must end with the string `{endswith}`.'
    include = 'The value `{value}` for `{key}` must include the string `{include}`.'
    exclude = 'The value `{value}` for `{key}` must not include the string `{exclude}`.'
    isalnum = 'The value `{value}` for `{key}` must consist of letters and numbers.'
    isalpha = 'The value `{value}` for `{key}` must consist of letters.'
    isdecimal = 'The value `{value}` for `{key}` must consist of decimal numbers.'
    isdigit = 'The value `{value}` for `{key}` must consist of numbers.'
    isidentifier = 'The value `{value}` for `{key}` must be a valid identifier.'
    islower = 'The alphabetical part of `{value}` for `{key}` must be all in lowercase.'
    isupper = 'The alphabetical part of `{value}` for `{key}` must be all in uppercase.'
    isprintable = 'The value `{value}` for `{key}` cannot be entirely printable.'
    isspace = 'The value `{value}` for `{key}` must consist of whitespace characters.'
    istitle = 'The value `{value}` for `{key}` must be in title case.'
    regex = 'The value `{value}` of `{key}` does not satisfy the regular rule `{regex}`.'
