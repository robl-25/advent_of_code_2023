from collections import Counter
from collections.abc import Iterable
from itertools import combinations


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


def expand_lines(matrix):
    lines_to_duplicate = []

    for row, line in enumerate(matrix):
        counter = Counter(line)
        if len(counter) == 1 and '.' in counter:
            lines_to_duplicate.append(row)

    idx_offset = 0
    for row in lines_to_duplicate:
        matrix.insert(row + idx_offset, ['.'] * len(matrix[0]))
        idx_offset += 1

    return matrix


def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    transposed_matrix = []

    for _ in range(cols):
        transposed_matrix.append([None] * rows)

    for (x, y), item in enumerate_n(matrix, n=2):
        transposed_matrix[y][x] = item

    return transposed_matrix


with open('input.txt') as f:
    matrix = [list(l) for l in f.read().splitlines()]

matrix = expand_lines(matrix)
matrix = transpose_matrix(matrix)
matrix = expand_lines(matrix)
matrix = transpose_matrix(matrix)

galaxies = [idx for idx, item in enumerate_n(matrix, n=2) if item == '#']
distances = 0
for galaxy_a, galaxy_b in combinations(galaxies, 2):
    diff_rows = abs(galaxy_a[0] - galaxy_b[0])
    diff_cols = abs(galaxy_a[1] - galaxy_b[1])

    distances += diff_rows + diff_cols

print(distances)