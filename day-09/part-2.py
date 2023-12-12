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

    result = 0
    for sub in reversed([s[0] for s in sub_sequences]):
        result = sub - result

    return result


with open('input.txt') as f:
    lines = f.read().splitlines()

sequences = []

for line in lines:
    sequences.append([int(i) for i in line.split()])

total = 0
for sequence in sequences:
    result = find_next(sequence)
    total += result

print(total)