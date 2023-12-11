from itertools import islice
from collections import Counter


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


with open('day-9/input.txt') as f:
    lines = f.read().splitlines()

sequences = []

for line in lines:
    sequences.append([int(i) for i in line.split()])

total = 0
for sequence in sequences:
    result = find_next(sequence)
    total += result

print(total)