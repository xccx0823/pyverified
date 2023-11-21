from typing import Union, Dict

from pyverify.rule.base import RuleBase


class Verify:
    """校验"""

    def __init__(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase], *, many: bool = False):
        self.data = data
        self.rules = rules

        #: 如果设置为True，则标识需要校验的数据是forloop的数据
        if many:
            for _data in data:
                self._verify(_data, rules)
        else:
            self._verify(data, rules)

    def _verify(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase]):
        pass
