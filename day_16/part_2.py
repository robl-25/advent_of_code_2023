from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field
from itertools import chain


@dataclass
class Node:
    symbol: str
    coords: tuple
    energized: bool=False
    directions_passed: set=field(default_factory=set)

    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    def energize(self, direction):
        if direction in self.directions_passed:
            return []

        self.directions_passed.add(direction)
        self.energized = True

        directions = {
            '.': self._empty_space,
            '/': self._mirror_tilt_right,
            '\\': self._mirror_tilt_left,
            '|': self._splitter_lines,
            '-': self._splitter_columns,
        }

        return directions[self.symbol](direction)

    def unenergize(self):
        self.directions_passed = set()
        self.energized = False

    def _normal_next(self, direction):
        return (self.coords[0] + direction[0], self.coords[1] + direction[1])

    def _empty_space(self, direction):
        return [self._normal_next(direction)]

    def _mirror_tilt_right(self, direction):
        # Going right. Reflected up.
        if direction[1] == 1:
            return [self._normal_next(self.directions['up'])]

        # Going left. Reflected down.
        if direction[1] == -1:
            return [self._normal_next(self.directions['down'])]

        # Going down. Reflected left.
        if direction[0] == 1:
            return [self._normal_next(self.directions['left'])]

        # Going up. Reflected right.
        if direction[0] == -1:
            return [self._normal_next(self.directions['right'])]

    def _mirror_tilt_left(self, direction):
        # Going right. Reflected down.
        if direction[1] == 1:
            return [self._normal_next(self.directions['down'])]

        # Going left. Reflected up.
        if direction[1] == -1:
            return [self._normal_next(self.directions['up'])]

        # Going down. Reflected right.
        if direction[0] == 1:
            return [self._normal_next(self.directions['right'])]

        # Going up. Reflected left.
        if direction[0] == -1:
            return [self._normal_next(self.directions['left'])]

    def _splitter_columns(self, direction):
        # Vertical beam. Split into horizontal beams.
        if direction[0] != 0:
            return [
                self._normal_next(self.directions['left']),
                self._normal_next(self.directions['right'])
            ]

        return [self._normal_next(direction)]

    def _splitter_lines(self, direction):
        # Horizontal beam. Split into vertical beams.
        if direction[1] != 0:
            return [
                self._normal_next(self.directions['up']),
                self._normal_next(self.directions['down'])
            ]

        return [self._normal_next(direction)]


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


def is_inside(coords, matrix):
    row, col = coords

    row_range = range(len(matrix))
    col_range = range(len(matrix[0]))

    return row in row_range and col in col_range


def energize_matrix(starting_node, starting_direction, matrix):
    next_nodes = [
        (starting_node.coords, starting_node.energize(starting_direction))
    ]

    for current_coords, next_coords in next_nodes:
        for i, j in next_coords:
            if not is_inside((i, j), matrix):
                continue

            direction = (i - current_coords[0], j - current_coords[1])
            result = matrix[i][j].energize(direction)
            next_nodes.append([(i, j), result])


def unenergize_matrix(matrix):
    for _, node in enumerate_n(matrix, n=2):
        node.unenergize()


def matrix_energy(matrix):
    return sum(1 for _, node in enumerate_n(matrix, n=2) if node.energized)


with open('input.txt') as file:
    matrix = [list(line) for line in file.read().splitlines()]

for (i, j), symbol in enumerate_n(matrix, n=2):
    matrix[i][j] = Node(symbol=symbol, coords=(i, j))


row_range = range(len(matrix))
col_range = range(len(matrix[0]))
max_energy = 0

# First row. Going down.
for y in col_range:
    energize_matrix(matrix[0][y], (1, 0), matrix)
    total_energy = matrix_energy(matrix)

    if total_energy > max_energy:
        max_energy = total_energy

    unenergize_matrix(matrix)

# Last row. Going up.
for y in col_range:
    energize_matrix(matrix[-1][y], (-1, 0), matrix)
    total_energy = matrix_energy(matrix)

    if total_energy > max_energy:
        max_energy = total_energy

    unenergize_matrix(matrix)

# First column. Going left.
for x in row_range:
    energize_matrix(matrix[x][0], (0, 1), matrix)
    total_energy = matrix_energy(matrix)

    if total_energy > max_energy:
        max_energy = total_energy

    unenergize_matrix(matrix)

# Last column. Going right.
for x in row_range:
    energize_matrix(matrix[x][-1], (0, -1), matrix)
    total_energy = matrix_energy(matrix)

    if total_energy > max_energy:
        max_energy = total_energy

    unenergize_matrix(matrix)


print(max_energy)