class Message:
    """Define check exception information."""
    # special type
    email = 'The current parameter string is not a mailbox.'
    phone = 'The current parameter string is not a phone number.'
    ipv4 = 'The current parameter string is not an ipv4 address.'
    ipv6 = 'The current parameter string is not an ipv6 address.'
    address = 'The current parameter string is not the link address.'

    # common
    required = 'The current parameter is required.'
    allow_none = 'The current argument cannot be an empty string or None value.'
    many = 'You set mang to True, but the type of the check data is not list or set or tuple.'
    multi = 'The data type of the data to be verified is not list or set or tuple.'
    enum = 'The value is not in the enumeration range.'
    gt = 'The value of {key} must be greater than {gt}'
    gte = 'The value of {key} must be at least {gte}'
    lt = 'The value of {key} must be less than {lt}'
    lte = 'The value of {key} must be less than or equal to {lte}'

    # frame
    params = 'The request parameter must be dict.'

    # type
    typeBool = 'The value is not of bool type.'
    typeInt = 'The value is not of int type.'
    typeFloat = 'The value is not of float type.'

    # bool
    convert = 'The string value cannot be converted to bool.'

    # str
    minLength = ''
    maxLength = ''
    startswith = ''
    endswith = ''
    include = ''
    exclude = ''
    isalnum = ''
    isalpha = ''
    isdecimal = ''
    isdigit = ''
    isidentifier = ''
    islower = ''
    isupper = ''
    isprintable = ''
    isspace = ''
    istitle = ''

    @classmethod
    def reload(cls, clss):
        msgs = dict(filter(lambda x: not x[0].startswith('__'), vars(clss).items()))
        for key, msg in msgs.items():
            setattr(cls, key, msg)
