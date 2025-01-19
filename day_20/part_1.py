from dataclasses import dataclass, field
from typing import Union


@dataclass
class Module:
    name: str
    neighbors: Union['Module', str]
    low_pulses: int = 0
    high_pulses: int = 0

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
            self.high_pulses += len(self.neighbors)
            return 1

        self.low_pulses += len(self.neighbors)
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
            self.low_pulses += len(self.neighbors)
            return 0

        self.high_pulses += len(self.neighbors)
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
        self.low_pulses += len(self.neighbors) + 1
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

for _ in range(1_000):
    queue = [(broadcaster, 'button', 0)]

    while queue:
        current_module, sender, pulse = queue.pop()

        if isinstance(current_module, str):
            continue

        next_pulse = current_module.process_pulse(pulse, sender)

        if next_pulse is None:
            continue

        for n in current_module.neighbors:
            queue.append((n, current_module, next_pulse))

total_low = sum(module.low_pulses for module in modules.values())
total_high = sum(module.high_pulses for module in modules.values())

print(total_low * total_high)