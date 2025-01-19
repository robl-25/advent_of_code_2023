from pprint import pp
from itertools import product

class Digit:
    def __init__(self, coord, value):
        self.coords = [coord]
        self.value = value

    def __repr__(self):
        return f'PartNumber(start={self.coords[0]}, end={self.coords[-1]}, value={self.value})'

    def add(self, coord, value):
        self.coords.append(coord)
        self.value += value

    def adjacent_coords(self, matrix):
        first_line = max(self.coords[0][0] - 1, 0)
        last_line = min(self.coords[0][0] + 1, len(matrix) - 1)

        first_column = max(self.coords[0][1] - 1, 0)
        last_column = min(self.coords[-1][1] + 1, len(matrix[0]) - 1)

        return product(range(first_line, last_line + 1), range(first_column, last_column + 1))

    def has_symbol(self, matrix):
        for i, j in self.adjacent_coords(matrix):
            if not matrix[i][j].isdigit() and matrix[i][j] != '.':
                return True

        return False


class Gear:
    def __init__(self, coord):
        self.coord = coord

    def collide_with(self, digit, matrix):
        if self.coord in digit.adjacent_coords(matrix):
          return True

        return False


def get_digits(matrix):
    numbers = []

    for i, line in enumerate(matrix):
        digit = None

        for j, col in enumerate(line):
            if col.isdigit() and digit is None:
                digit = Digit((i, j), col)
            elif col.isdigit() and digit is not None:
                digit.add((i, j), col)
            elif digit is not None and not col.isdigit():
                numbers.append(digit)
                digit = None

        if digit is not None:
            numbers.append(digit)

    return numbers


def get_gears(matrix):
    gears = []

    for i, line in enumerate(matrix):
        for j, col in enumerate(line):
          if col == '*':
              gears.append(Gear((i,j)))

    return gears


with open('input.txt') as file:
    matrix = [list(line.strip()) for line in file]
    numbers = get_digits(matrix)
    gears = get_gears(matrix)
    result = 0

    for gear in gears:
        integers = [number.value for number in numbers if gear.collide_with(number, matrix)]

        if len(integers) == 2:
            result += int(integers[0]) * int(integers[1])

    pp(result)