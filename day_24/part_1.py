from dataclasses import dataclass
from itertools import combinations
from fractions import Fraction

LIMIT_MIN=200_000_000_000_000
LIMIT_MAX=400_000_000_000_000


@dataclass
class Hailstone:
    initial_position: tuple
    speed: tuple

    def __post_init__(self):
        speed_x, speed_y, _ = self.speed
        pos_x, pos_y, _ = self.initial_position

        self.b = (speed_y + pos_y - ((speed_x + pos_x) * pos_y / pos_x)) / (1 - ((speed_x + pos_x) / pos_x))
        self.a = (pos_y - self.b) / pos_x

    def crosses(self, other):
        if (self.a - other.a) == 0:
            return False

        crossing_x = (other.b - self.b) / (self.a - other.a)
        crossing_y = (self.a * crossing_x) + self.b

        return (
            crossing_x >= LIMIT_MIN and crossing_x <= LIMIT_MAX
            and crossing_y >= LIMIT_MIN and crossing_y <= LIMIT_MAX
            and self._time(crossing_x) >= 0
            and other._time(crossing_x) >= 0
        )

    def _time(self, crossing_x):
        return (crossing_x - self.initial_position[0]) / self.speed[0]


with open('input.txt') as f:
    data = f.readlines()

hailstones = []

for line in data:
    position, speed = line.strip().split('@')

    position = [Fraction(p) for p in position.split(', ')]
    speed = [Fraction(s) for s in speed.split(', ')]

    hailstones.append(
        Hailstone(
            initial_position=tuple(position),
            speed=tuple(speed)
        )
    )

print(sum(a.crosses(b) for a, b in combinations(hailstones, 2)))
