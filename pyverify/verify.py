from typing import Union, Dict as Dic

from pyverify._unset import unset
from pyverify.exc import ValidationError
from pyverify.msg import Message
from pyverify.rules.base import RuleBase
from pyverify.rules.underlying import List, Dict


class Verify:

    def __init__(self, data: Union[dict, list, set, tuple], rules: Dic[str, RuleBase], *, many: bool = False):
        self.data = data
        self.rules = rules

        # If set to True, the data to be verified is cyclic data.
        if many:
            verify_data = []

            if not isinstance(data, (list, set, tuple)):
                raise ValidationError(Message.many)

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
            if isinstance(rule, (List, Dict)):

                #: rule dest
                if rule.dest is True:
                    verify_data[key] = value
                    continue

                #: blanket rules
                #: - required
                #: - allow_none
                #: - default
                rule.common_rules_verify(key, value)

                #: rule multi: Used to distinguish Dict from List.
                if rule.multi:
                    if isinstance(value, (list, set, tuple)):
                        raise ValidationError(Message.multi.format(key=key, value=value))
                    for _value in value:
                        verify_data[key] = self.verify(_value, rule.subset)
                else:
                    verify_data[key] = self.verify(value, rule.subset)

            # Data rule analysis.
            else:
                verify_data[key] = rule.parse(key, value)

        return verify_data
