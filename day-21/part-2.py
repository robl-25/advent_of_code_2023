from collections.abc import Iterable
from itertools import islice
from collections import Counter


STEPS = 26_501_365



def sliding_window(iterable, n=2):
    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)


def all_equal(iterable):
    return len(Counter(iterable)) == 1


def find_next(sequence):
    sub_sequences = [sequence]

    for s in sub_sequences:
        diffs = [b - a for a, b in sliding_window(s)]
        sub_sequences.append(diffs)

        if all_equal(diffs):
            break

    return sum(s[-1] for s in sub_sequences)


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


def find_node(matrix, value):
    return next(coords for coords, item in enumerate_n(matrix, n=2) if item == value)


def node_neighbors(node, matrix):
    x, y = node

    neighbors = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

    return [n for n in neighbors if matrix[n[0] % len(matrix)][n[1] % len(matrix[0])] != '#']


with open('input.txt') as file:
    matrix = [list(line) for line in file.read().splitlines()]

start_node = find_node(matrix, 'S')
total_steps = 65
sequence = []

for i in range(3):
    queue = [{start_node}]
    total_steps = 65 + 131 * i

    steps = 0
    while steps < total_steps:
        current_nodes = queue.pop()

        next_nodes = set()

        for current_node in current_nodes:
            for neighbor in node_neighbors(current_node, matrix):
                next_nodes.add(neighbor)

        queue.append(next_nodes)

        steps += 1

    sequence.append(len(next_nodes))

print(sequence)

i = 3
while steps <= STEPS:
    i += 1
    steps = 65 + 131 * i
    sequence.append(find_next(sequence))
    print(f'{(steps/STEPS) * 100:.3f}%', end='\r')

print(sequence[-1])