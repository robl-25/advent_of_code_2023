from collections.abc import Iterable


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


def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    transposed_matrix = []

    for _ in range(cols):
        transposed_matrix.append([None] * rows)

    for (x, y), item in enumerate_n(matrix, n=2):
        transposed_matrix[y][x] = item

    return transposed_matrix


def roll_rocks(l):
    valid_spaces = 0

    for i, item in enumerate(l):
        if item == '#':
            valid_spaces = 0

        if item == '.':
            valid_spaces += 1

        if item == 'O':
            l[i] = '.'
            l[i - valid_spaces] = 'O'


with open('input.txt') as file:
    matrix = [list(l) for l in file.read().splitlines()]

matrix = transpose_matrix(matrix)

for line in matrix:
    roll_rocks(line)

matrix = transpose_matrix(matrix)

score = 0
for i, line in enumerate(matrix):
    score += line.count('O') * (len(matrix) - i)

print(score)