from typing import Union, Dict

from pyverify._unset import unset
from pyverify.rule.base import RuleBase
from pyverify.rule.underlying import Flat


class Verify:
    """校验"""

    def __init__(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase], *, many: bool = False):
        self.data = data
        self.rules = rules

        #: 如果设置为True，则标识需要校验的数据是forloop的数据
        if many:
            for _data in data:
                self.verify(_data, rules)
        else:
            self.verify(data, rules)

    def verify(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase]):

        verify_data = {}

        for key, rule in rules:
            # 通过反射获取对应的值
            value = getattr(data, key, unset)

            # 嵌套结构处理，触发递归解析结果
            if isinstance(rule, Flat):
                if Flat.multi:
                    for _value in value:
                        verify_data[key] = self.verify(_value, rule.subset)
                else:
                    verify_data[key] = self.verify(value, rule.subset)

            # 数据规则解析
            else:
                verify_data[key] = rule.parse(key, value)

        return verify_data
