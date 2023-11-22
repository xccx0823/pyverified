from typing import Union, Dict

from pyverify._unset import unset
from pyverify.rules.base import RuleBase
from pyverify.rules.underlying import Struct


class Verify:
    """校验"""

    def __init__(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase], *, many: bool = False):
        self.data = data
        self.rules = rules

        #: 如果设置为True，则标识需要校验的数据是forloop的数据
        if many:
            verify_data = []
            for _data in data:
                verify_data.append(self.verify(_data, rules))
        else:
            verify_data = self.verify(data, rules)

        self.params = verify_data

    def verify(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase]):

        verify_data = {}

        for key, rule in rules.items():
            # 不为字典时，通过反射获取对应的值
            if isinstance(data, dict):
                value = data.get(key, unset)
            else:
                value = getattr(data, key, unset)

            # 嵌套结构处理，触发递归解析结果
            if isinstance(rule, Struct):

                # TODO:处理flat类型的规则

                if rule.multi:
                    for _value in value:
                        verify_data[key] = self.verify(_value, rule.subset)
                else:
                    verify_data[key] = self.verify(value, rule.subset)

            # 数据规则解析
            else:
                verify_data[key] = rule.parse(key, value)

        return verify_data
