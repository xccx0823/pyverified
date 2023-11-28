NOT_UNPACK = 0
LIST_UNPACK = 1
DICT_UNPACK = 2


def for_params(func, iteration, *, unpack=NOT_UNPACK):
    unpack_functions = {NOT_UNPACK: func, LIST_UNPACK: lambda x: func(*x), DICT_UNPACK: lambda x: func(**x)}
    for item in iteration:
        unpack_functions[unpack](item)
