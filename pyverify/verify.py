from typing import Union, Dict

from pyverify.exc import Error, VerifyError
from pyverify.rule.base import RuleBase


class Verify:
    """校验"""

    def __init__(self, data: Union[dict, list, set, tuple], rules: Dict[str, RuleBase], *, many: bool = False):
        #: 需要校验的数据
        self.data = data

        #: 如果设置为True，则标识需要校验的数据是forloop的数据
        self.many = many

        #: 定义的规则
        self.rules = rules

        #: 收集错误的对象
        self.err = Error()

    def is_valid(self, raise_exception=False):
        # 校验规则
        self._verify()

        # 触发错误异常
        isnull = self.err.isnull()
        if not isnull and raise_exception:
            raise VerifyError(self.err)

        return isnull

    def _verify(self):
        pass
