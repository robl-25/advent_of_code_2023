from dataclasses import dataclass
import operator


@dataclass
class Rule:
    attribute: str
    operation: str
    value: int
    target: str

    def __post_init__(self):
        ops = {
            '>': operator.gt,
            '<': operator.lt
        }

        self._operator = ops[self.operation]

    def is_applicable(self, part):
        part_attr = part.__getattribute__(self.attribute)

        return self._operator(part_attr, self.value)


@dataclass
class Workflow:
    name: str
    rules: [Rule]
    default_destination: str

    def process_part(self, part):
        rule = next((rule for rule in self.rules if rule.is_applicable(part)), None)

        if not rule:
            return self.default_destination

        return rule.target


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def sum_attr(self):
        return self.x + self.m + self.a + self.s


with open('input.txt') as file:
    input = file.read().splitlines()

empty_string = input.index('')
instructions = input[:empty_string]
input_parts = input[empty_string + 1:]
workflows = {}

for instruction in instructions:
    name = instruction.split('{')[0]
    rule_desc = instruction.split('{')[-1].strip('}').split(',')
    rules = []

    for description in rule_desc[:-1]:
        attribute = description[0]
        operation = description[1]
        value, target = description[2:].split(':')

        rules.append(Rule(
            attribute=attribute,
            operation=operation,
            value=int(value),
            target=target
        ))

    w = Workflow(name=name, default_destination=rule_desc[-1], rules=rules)
    workflows[w.name] = w

total_accepted = 0
for p in input_parts:
    x, m, a, s = [int(item.split('=')[1]) for item in p.strip('{}').split(',')]

    part = Part(x=x, s=s, m=m, a=a)

    current_workflow = workflows['in']

    while current_workflow not in ['A', 'R']:
        target = current_workflow.process_part(part)

        current_workflow = target

        if target in workflows:
            current_workflow = workflows[target]

    if current_workflow == 'A':
        total_accepted += part.sum_attr()

print(total_accepted)