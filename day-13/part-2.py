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


def edit_distance(s0, s1):
    return sum(1 for a, b in zip(s0, s1) if a != b)


def check_smudged_line(line, n):
    if n < len(line) / 2:
        return edit_distance(line[:n], line[n: 2 * n][::-1]) == 1

    if n > len(line) / 2:
        l = line[::-1]
        n = len(line) - n

        return edit_distance(l[:n], l[n: 2 * n][::-1]) == 1

    return edit_distance(line, line[::-1]) == 1


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

    return mirrors


def matrix_score(matrix, transpose=False):
    if transpose:
        matrix = transpose_matrix(matrix)

    mirrors = find_mirror(matrix[0]) | find_mirror(matrix[1])

    if not mirrors:
        return 0

    mirror_score = dict.fromkeys(mirrors, set())

    for mirror in mirrors:
        mirror_score[mirror] = {line_idx for line_idx, line in enumerate(matrix) if check_line(line, mirror)}

    missing_one_line = {k: v for k, v in mirror_score.items() if len(v) == len(matrix) - 1}

    if not missing_one_line:
        return 0

    s = set(range(len(matrix)))
    missing_one_line = [mirror for mirror, lines in missing_one_line.items() if check_smudged_line(matrix[(s - lines).pop()], mirror)]

    if not missing_one_line:
        return 0

    if transpose:
        return missing_one_line[0] * 100

    return missing_one_line[0]


with open('input.txt') as f:
    matrixes = [m.splitlines() for m in f.read().split('\n\n')]

result = []
for matrix in matrixes:
    score = matrix_score(matrix)

    if score == 0:
        score = matrix_score(matrix, transpose=True)

    result.append(score)

print(sum(result))