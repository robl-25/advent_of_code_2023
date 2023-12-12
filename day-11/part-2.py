from collections import Counter
from collections.abc import Iterable
from itertools import combinations


EXPANDING_FACTOR = 999_999


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


def expanding_lines_indexes(matrix):
    lines_to_duplicate = []

    for row, line in enumerate(matrix):
        counter = Counter(line)
        if len(counter) == 1 and '.' in counter:
            lines_to_duplicate.append(row)

    return lines_to_duplicate


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

rows_to_duplicate = expanding_lines_indexes(matrix)
matrix = transpose_matrix(matrix)

cols_to_duplicate = expanding_lines_indexes(matrix)
matrix = transpose_matrix(matrix)

galaxies = [idx for idx, item in enumerate_n(matrix, n=2) if item == '#']

distances = 0
for galaxy_a, galaxy_b in combinations(galaxies, 2):
    first_row, last_row = sorted([galaxy_a[0], galaxy_b[0]])
    row_range = range(first_row, last_row)

    first_col, last_col = sorted([galaxy_a[1], galaxy_b[1]])
    col_range = range(first_col, last_col)

    crossing_rows = sum(1 for row in rows_to_duplicate if row in row_range)
    crossing_cols = sum(1 for col in cols_to_duplicate if col in col_range)

    diff_rows = abs(galaxy_a[0] - galaxy_b[0])
    diff_cols = abs(galaxy_a[1] - galaxy_b[1])

    distance = diff_rows + diff_cols
    distance += (crossing_rows) * EXPANDING_FACTOR
    distance += (crossing_cols) * EXPANDING_FACTOR

    distances += distance

print(distances)