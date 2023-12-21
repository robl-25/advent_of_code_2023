import copy
import math
import operator

from dataclasses import dataclass
from typing import Union


@dataclass
class Rule:
    attribute: str
    operation: str
    value: int
    success: Union['Rule', str]
    failure: Union['Rule', str] = None

    final_states = {'A', 'R'}

    @classmethod
    def build(cls, description):
        attribute, operation = description[0], description[1]
        value, success = description[2:].split(':')

        return cls(
            attribute=attribute,
            operation=operation,
            value=int(value),
            success=success
        )

    def get_success(self, tagged_rules):
        if isinstance(self.success, Rule) or self.success in self.final_states:
            return self.success

        return tagged_rules[self.success]

    def get_failure(self, tagged_rules):
        if isinstance(self.failure, Rule) or self.failure in self.final_states:
            return self.failure

        return tagged_rules[self.failure]

    def append_failure(self, failure):
        self.failure = failure


class Part:
    operators = {
        '>': operator.gt,
        '<': operator.lt
    }

    def __init__(self):
        self.ranges = {
            'x': [i for i in range(1, 4_001)],
            'm': [i for i in range(1, 4_001)],
            'a': [i for i in range(1, 4_001)],
            's': [i for i in range(1, 4_001)]
        }

    def restrict(self, rule):
        op = self.operators[rule.operation]
        self.ranges[rule.attribute] = [i for i in self.ranges[rule.attribute] if op(i, rule.value)]

    def reverse_restrict(self, rule):
        op = self.operators[rule.operation]
        self.ranges[rule.attribute] = [i for i in self.ranges[rule.attribute] if not op(i, rule.value)]

    def possibilities(self):
        return math.prod(len(r) for r in self.ranges.values())


with open('input.txt') as file:
    input = file.read().splitlines()
    separator_idx = input.index('')
    workflow_descs = input[:separator_idx]

# "workflows"
tagged_rules = {}
all_rules = []

for workflow_desc in workflow_descs:
    tag, rest = workflow_desc.split('{')
    rule_descs = rest.strip('}').split(',')

    rules = []

    # First rule must be tagged with the workflow name
    first_rule = Rule.build(rule_descs[0])
    tagged_rules[tag] = first_rule

    rules.append(first_rule)

    for idx, rule_desc in enumerate(rule_descs[1:-1]):
        rule = Rule.build(rule_desc)

        # Add the current rule as the failure path for the previous one
        rules[idx].append_failure(rule)
        rules.append(rule)

    # The failure case of the last rule in a workflow points to either:
    #   - a tagged rule; or
    #   - A; or
    #   - R.
    #
    rules[-1].append_failure(rule_descs[-1])

    all_rules.extend(rules)

total_possibilities = 0
queue = [(Part(), tagged_rules['in'])]

while queue:
    part, rule = queue.pop()

    if rule == 'A':
        total_possibilities += part.possibilities()
        continue

    if rule == 'R':
        continue

    # Move to the success neighbor
    success_rule = rule.get_success(tagged_rules)

    success_part = copy.deepcopy(part)
    success_part.restrict(rule)

    if all(success_part.ranges.values()):
        queue.append((success_part, success_rule))

    # Move to the failure neighbor
    failure_rule = rule.get_failure(tagged_rules)

    failure_part = copy.deepcopy(part)
    failure_part.reverse_restrict(rule)

    if all(failure_part.ranges.values()):
        queue.append((failure_part, failure_rule))

print(f'{total_possibilities}')