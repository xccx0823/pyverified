from typing import Union, Dict as Dic

from pyverified import ValidationError, msg
from pyverified.verify._unset import unset
from pyverified.verify.base import RuleBase
from pyverified.verify.type_ import List, Dict


class Verify:

    def __init__(self, data: Union[dict, list, set, tuple], rules: Dic[str, RuleBase], *, many: bool = False):
        self.data = data
        self.rules = rules

        # If set to True, the data to be verified is cyclic data.
        if many:
            verify_data = []

            if not isinstance(data, (list, set, tuple)):
                raise ValidationError(msg.message.many)

            for _data in data:
                verify_data.append(self.verify(_data, rules))
        else:
            verify_data = self.verify(data, rules)

        self.params = verify_data

    def verify(self, data: Union[dict, list, set, tuple], rules: Dic[str, RuleBase]):

        verify_data = {}

        for key, rule in rules.items():

            # If it is not a dictionary, the corresponding value is obtained by reflection.
            if isinstance(data, dict):
                value = data.get(key, unset)
            else:
                value = getattr(data, key, unset)

            # Nested structure processing, triggering recursive parsing results.
            if isinstance(rule, List):
                if not isinstance(value, (list, set, tuple)):
                    raise ValidationError(msg.message.multi.format(key=key, value=value))
                if rule.dest is True:
                    verify_data[key] = value
                    continue
                rule.common_rules_verify(key, value)
                verify_values = []
                for _value in value:
                    verify_values.append(self.verify(_value, rule.subset))
                verify_data[key] = verify_values

            elif isinstance(rule, Dict):
                if rule.dest is True:
                    verify_data[key] = value
                    continue
                rule.common_rules_verify(key, value)
                verify_data[key] = self.verify(value, rule.subset)

            # Data rule analysis.
            else:
                verify_data[key] = rule.execute_parse(key, value)

        return verify_data
