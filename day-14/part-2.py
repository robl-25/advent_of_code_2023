import copy
import time
from collections.abc import Iterable


CYCLE_NUMBER=1_000


def roll_rocks_south(matrix):
    row_range = range(len(matrix) - 1, -1, -1)
    col_range = range(0, len(matrix[0]))

    for j in col_range:
        valid_spaces = 0

        for i in row_range:
            item = matrix[i][j]

            if item == '#':
                valid_spaces = 0

            if item == '.':
                valid_spaces += 1

            if item == 'O':
                matrix[i][j] = '.'
                matrix[i + valid_spaces][j] = 'O'


def roll_rocks_north(matrix):
    row_range = range(0, len(matrix))
    col_range = range(0, len(matrix[0]))

    for j in col_range:
        valid_spaces = 0

        for i in row_range:
            item = matrix[i][j]

            if item == '#':
                valid_spaces = 0

            if item == '.':
                valid_spaces += 1

            if item == 'O':
                matrix[i][j] = '.'
                matrix[i - valid_spaces][j] = 'O'


def roll_rocks_east(matrix):
    for line in matrix:
        valid_spaces = 0

        for i, item in zip(range(len(line) - 1, -1, -1), reversed(line)):
            if item == '#':
                valid_spaces = 0

            if item == '.':
                valid_spaces += 1

            if item == 'O':
                line[i] = '.'
                line[i + valid_spaces] = 'O'


def roll_rocks_west(matrix):
    for line in matrix:
        valid_spaces = 0

        for i, item in enumerate(line):
            if item == '#':
                valid_spaces = 0

            if item == '.':
                valid_spaces += 1

            if item == 'O':
                line[i] = '.'
                line[i - valid_spaces] = 'O'


def line_score(l):
    score = 0

    for i, item in enumerate(l):
        if item == 'O':
            score += len(l)


def cycle_platform(matrix):
    roll_rocks_north(matrix)
    roll_rocks_west(matrix)
    roll_rocks_south(matrix)
    roll_rocks_east(matrix)


with open('input.txt') as file:
    matrix = [list(l) for l in file.read().splitlines()]


start = time.time()
for n in range(CYCLE_NUMBER):
    cycle_platform(matrix)

score = 0
for i, line in enumerate(matrix):
    score += line.count('O') * (len(matrix) - i)

print(score)