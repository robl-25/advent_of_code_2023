from dataclasses import dataclass
from dataclasses import field
from functools import cache

import heapq
import sys

sys.setrecursionlimit(1_000_000)


@dataclass
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    visited: bool=False
    distance: int=float('-inf')

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    slopes = {
        '>': 'east',
        '<': 'west',
        'v': 'south',
        '^': 'north'
    }

    # Gets neighbor in `self.matrix` given a `direction`.
    def _neighbor(self, direction):
        neighbor_coords = (
            self.coords[0] + self.directions[direction][0],
            self.coords[1] + self.directions[direction][1]
        )

        if neighbor_coords[0] not in range(len(self.matrix)):
            return None

        if neighbor_coords[1] not in range(len(self.matrix[0])):
            return None

        neighbor = self.matrix[neighbor_coords[0]][neighbor_coords[1]]

        if neighbor.symbol == 'v' and direction == 'north':
            return None

        if neighbor.symbol == '>' and direction == 'west':
            return None

        if neighbor.symbol == '^' and direction == 'south':
            return None

        if neighbor.symbol == '<' and direction == 'east':
            return None

        return neighbor

    # All neighbors in `self.directions`.
    def neighbors(self):
        if self.symbol in self.slopes:
            n = [self._neighbor(self.slopes[self.symbol])]
        else:
            n = [self._neighbor(direction) for direction in self.directions]

        return [neighbor for neighbor in n if neighbor is not None]

    def manhattan_distance(self, other):
        return abs(self.coords[0] - other.coords[0]) + abs(self.coords[1] - other.coords[1])

    def a_star_score(self, target_node):
        return (self.distance + self.manhattan_distance(target_node)) * -1

    # Makes nodes equal if they have the same `coords`.
    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return (self.distance * -1) < (other.distance * -1)

    def __repr__(self):
        return self.symbol

    def __hash__(self):
        return hash(self.coords)

    def reset(self):
        self.visited = False
        self.distance = float('-inf')


def enumerate_n(iterable, start=0, n=1):
    from collections.abc import Iterable

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

@cache
def backtrack(current_node, target, distance=0):
    if current_node == target:
        return distance

    distances = []

    for neighbor in current_node.neighbors():
        if neighbor.visited or neighbor.symbol == '#':
            continue

        neighbor.visited = True
        distances.append(backtrack(neighbor, target, distance + 1))
        neighbor.visited = False

    return max(distances, default=-1)


with open('input.txt') as f:
    matrix = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

start = next(node for node in matrix[0] if node.symbol == '.')
end = next(node for node in matrix[-1] if node.symbol == '.')

distance = backtrack(start, end)

print(distance)
