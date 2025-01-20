from dataclasses import dataclass
from dataclasses import field
import bisect


@dataclass
class Brick:
    point_a: tuple
    point_b: tuple
    supports: set=field(default_factory=set, repr=False)
    supported_by: set=field(default_factory=set, repr=False)

    def __post_init__(self):
        self.mins = list(min(a, b) for a, b in zip(self.point_a, self.point_b))
        self.maxs = list(max(a, b) for a, b in zip(self.point_a, self.point_b))
        self.ranges = tuple(range(a, b + 1) for a, b in zip(self.mins, self.maxs))

    def collides(self, other):
        return bool(
            self.maxs[2] < other.mins[2]
            and set(other.ranges[0]) & set(self.ranges[0])
            and set(other.ranges[1]) & set(self.ranges[1])
        )

    def removable(self):
        return all(len(b.supported_by) > 1 for b in self.supports)

    def __lt__(self, other):
        return self.mins[2] < other.mins[2]

    def __hash__(self):
        return hash(id(self))


with open('input.txt') as f:
    data = f.readlines()

bricks = []

for line in data:
    coords_a, coords_b = line.split('~')

    bricks.append(Brick(
        point_a=tuple(int(i) for i in coords_a.split(',')),
        point_b=tuple(int(i) for i in coords_b.split(','))
    ))

bricks.sort()

fallen_bricks = []

for brick in bricks:
    z_size = brick.maxs[2] - brick.mins[2]
    first_colling_brick = next((b for b in reversed(fallen_bricks) if b.collides(brick)), None)

    if first_colling_brick is None:
        brick.mins[2] = 1
    else:
        colliding_bricks = [b for b in fallen_bricks if b.maxs[2] == first_colling_brick.maxs[2] and b.collides(brick)]

        brick.supported_by |= set(colliding_bricks)

        for b in colliding_bricks:
            b.supports.add(brick)

        brick.mins[2] = first_colling_brick.maxs[2] + 1

    brick.maxs[2] = brick.mins[2] + z_size

    bisect.insort(fallen_bricks, brick, key=lambda b: b.maxs[2])

print(sum(brick.removable() for brick in bricks))
