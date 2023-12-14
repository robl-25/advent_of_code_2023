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


def check_line(line, n):
    if n < len(line) / 2:
        return line[:n] == line[n: 2 * n][::-1]

    if n > len(line) / 2:
        l = line[::-1]
        n = len(line) - n

        return l[:n] == l[n: 2 * n][::-1]

    return line == line[::-1]


def find_mirror(s):
    mirrors = set()

    for i, _ in enumerate(s):
        sub = s[i:]

        if sub == sub[::-1] and len(sub) % 2 == 0:
            mirrors.add(round(i + len(sub) / 2))

    s = s[::-1]

    for i, _ in enumerate(s):
        sub = s[i:]

        if sub == sub[::-1] and len(sub) % 2 == 0:
            mirrors.add(round((len(s) - i) / 2))

    return list(mirrors)


def matrix_score(matrix, transpose=False):
    if transpose:
        matrix = transpose_matrix(matrix)

    mirrors = find_mirror(matrix[0])

    if not mirrors:
        return 0

    score = 0
    for line in matrix[1:]:
        if not mirrors:
            break

        mirrors = [mirror for mirror in mirrors if check_line(line, mirror)]

    if len(mirrors) > 1:
        pp(matrix)
        print(f'Deu pau => {mirrors}')

    if not mirrors:
        return 0

    if transpose:
        return mirrors[0] * 100

    return mirrors[0]


with open('input.txt') as f:
    matrixes = [m.splitlines() for m in f.read().split('\n\n')]

result = []
for matrix in matrixes:
    score = matrix_score(matrix)

    if score == 0:
        score = matrix_score(matrix, transpose=True)
        if score == 0:
            pp(matrix)
            print('Deu ruim')

    result.append(score)

print(sum(result))