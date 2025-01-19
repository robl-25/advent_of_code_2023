from collections import Counter
from functools import lru_cache


FOLDING_FACTOR = 5


@lru_cache(maxsize=None)
def possibilities(s, mask):
    if not s and not mask:
        return 1

    counter = Counter(s)

    if counter.get('#', 0) + counter.get('?', 0) < sum(mask):
        return 0

    if counter.get('#', 0) > sum(mask):
        return 0

    s0 = s[0]

    if s0 == '.':
        return possibilities(s[1:], mask)

    if s0 == '#':
        sub_s = s[:mask[0]]
        sub_counter = Counter(sub_s)

        working_springs = sub_counter.get('#', 0) + sub_counter.get('?', 0)

        if working_springs < mask[0]:
            return 0

        if len(s) == mask[0]:
            last_character = 'EOF'
        else:
            last_character = s[mask[0]]

        if last_character not in {'.', '?', 'EOF'}:
            return 0

        return possibilities(s[mask[0] + 1:], mask[1:])

    return possibilities(s[1:], mask) + possibilities('#' + s[1:], mask)


def count_possibilities(line):
    data, mask = line.split(' ')

    data = '?'.join([data] * FOLDING_FACTOR)
    mask = tuple(int(i) for i in mask.split(',')) * FOLDING_FACTOR

    return possibilities(data, mask)


with open('input.txt') as file:
    lines = file.read().splitlines()

total = 0
for idx, line in enumerate(lines):
    total_line = count_possibilities(line)
    total += total_line

print(total)