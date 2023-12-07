class Message:
    """Define check exception information."""

    email = 'The current parameter string is not a mailbox.'
    telephone = 'The current parameter string is not a phone number.'
    ipv4 = 'The current parameter string is not an ipv4 address.'
    ipv6 = 'The current parameter string is not an ipv6 address.'
    address = 'The current parameter string is not the link address.'

    required = 'The current parameter is required.'
    allow_none = 'The current argument cannot be an empty string or None value.'
    many = 'You set mang to True, but the type of the check data is not list or set or tuple.'
    multi = 'The data type of the data to be verified is not list or set or tuple.'

    @classmethod
    def reload(cls, clss):
        msgs = dict(filter(lambda x: not x[0].startswith('__'), vars(clss).items()))
        for key, msg in msgs.items():
            setattr(cls, key, msg)
