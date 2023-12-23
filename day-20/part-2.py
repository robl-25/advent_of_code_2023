from dataclasses import dataclass, field
from typing import Union
from math import lcm
from collections import deque


@dataclass
class Module:
    name: str
    neighbors: Union['Module', str]

    @staticmethod
    def parse(line):
        name, neighbors = line.split(' -> ')
        neighbors = neighbors.split(', ')

        return (name, neighbors)


@dataclass
class FlipFlop(Module):
    state: bool = False

    @classmethod
    def build(cls, line):
        name, neighbors = super().parse(line)

        return cls(
            name=name[1:],
            neighbors=neighbors
        )

    def process_pulse(self, pulse, sender):
        if pulse == 1:
            return

        self.flip()

        if self.state:
            return 1

        return 0

    def flip(self):
        self.state = not self.state


@dataclass
class Conjunction(Module):
    state: dict = field(default_factory=dict)

    @classmethod
    def build(cls, line):
        name, neighbors = super().parse(line)

        return cls(
            name=name[1:],
            neighbors=neighbors
        )

    def process_pulse(self, pulse, sender):
        self.state[sender.name] = pulse

        if all(self.state.values()):
            return 0

        return 1


    def add_state(self, module_name):
        self.state[module_name] = 0


@dataclass
class Broadcaster(Module):
    @classmethod
    def build(cls, line):
        name, neighbors = super().parse(line)

        return cls(
            name=name,
            neighbors=neighbors
        )

    def process_pulse(self, pulse, _sender):
        return pulse


with open('input.txt') as file:
    lines = file.read().splitlines()

modules = {}
types = {
    'b': Broadcaster,
    '%': FlipFlop,
    '&': Conjunction
}

for line in lines:
    module = types[line[0]].build(line)
    modules[module.name] = module

high_values = {module.name: None for module in modules.values() if 'ql' in module.neighbors}

for module in modules.values():
    neighbors = []

    for n in module.neighbors:
        if n not in modules:
            neighbors.append(n)
            continue

        neighbors.append(modules[n])

        if isinstance(modules[n], Conjunction):
            modules[n].add_state(module.name)

    module.neighbors = neighbors

broadcaster = modules['broadcaster']
press = 0

while not all(value is not None for value in high_values.values()):
  queue = deque()
  press += 1

  queue.append((broadcaster, 'button', 0))

  while queue:
      current_module, sender, pulse = queue.popleft()

      if isinstance(current_module, str):
          continue

      if current_module.name == 'ql' and pulse == 1:
        if high_values[sender.name] is None:
          high_values[sender.name] = press

      next_pulse = current_module.process_pulse(pulse, sender)

      if next_pulse is None:
          continue

      for n in current_module.neighbors:
          queue.append((n, current_module, next_pulse))

print(lcm(*high_values.values()))
