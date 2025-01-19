from collections.abc import Iterable
from itertools import product

from dataclasses import dataclass
from dataclasses import field


@dataclass
class Pipe:
    symbol: str
    coords: tuple
    connecting_neighbors: set = field(default_factory=set)

    def populate_connected_nodes(self):
        connected_nodes = {
            '.': set(),
            'L': {self._up(), self._right()},
            '|': {self._up(), self._down()},
            '-': {self._left(), self._right()},
            '7': {self._left(), self._down()},
            'J': {self._up(), self._left()},
            'F': {self._down(), self._right()},
            'S': {self._up(), self._down(), self._left(), self._right()}
        }

        self.connecting_neighbors = connected_nodes[self.symbol]

    def _up(self):
        return (self.coords[0] - 1, self.coords[1])

    def _down(self):
        return (self.coords[0] + 1, self.coords[1])

    def _right(self):
        return (self.coords[0], self.coords[1] + 1)

    def _left(self):
        return (self.coords[0], self.coords[1] - 1)

    def __hash__(self):
        return hash(str(self))


def enumerate_n(iterable, start=0, n=1):
    count = start

    for item in iterable:
        if isinstance(item, Iterable) and n > 1:
            for index, value in enumerate_n(iter(item), start=start, n=n - 1):
                if not isinstance(index, Iterable):
                    index = [index]

                yield tuple([count, *index]), value
        else:
            yield count, item

        count += 1


with open('input.txt') as f:
    lines = f.read().splitlines()

matrix = [list(line) for line in lines]
starting_spot = None

for (x, y), symbol in enumerate_n(matrix, n=2):
    pipe = Pipe(symbol=symbol, coords=(x, y))
    pipe.populate_connected_nodes()

    if symbol == 'S':
        starting_spot = pipe

    matrix[x][y] = pipe

steps = 0
visited = set()
current_node = starting_spot

while current_node not in visited:
    visited.add(current_node)

    for row, col in current_node.connecting_neighbors:
        neighbor = matrix[row][col]
        if current_node.coords in neighbor.connecting_neighbors and neighbor not in visited:
            current_node = neighbor

print(len(visited) // 2)