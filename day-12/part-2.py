from functools import lru_cache


def group_equal(iterable):
    subgroups = []

    g = []
    for item in iterable:
        if not g or item == g[0]:
            g.append(item)
        else:
            subgroups.append(g)
            g = [item]

    if g:
        subgroups.append(g)

    return subgroups


def is_valid(data, mask):
    return tuple(len(g) for g in group_equal(data) if g[0] == '#') == mask


@lru_cache(maxsize=None)
def f(sub_data, data, mask, idx):
    if idx == len(data):
        if is_valid(sub_data, mask):
            return 1

        return 0

    next_idx = max(data.find('?', idx + 1), idx + 1)

    if next_idx > len(data):
        next_idx = len(data)

    if data[idx] == '?':
        case_1 = f(sub_data + '#', data, mask, next_idx)
        case_2 = f(sub_data + '.', data, mask, next_idx)

        return case_1 + case_2

    return f(sub_data + data[idx:next_idx], data, mask, next_idx)



def count_possibilities(line):
    data, mask = line.split(' ')

    mask = tuple(int(i) for i in mask.split(','))

    result = f('', data, mask, 0)

    print(f'{line} => {result}')

    return result


with open('input.txt') as file:
    lines = file.read().splitlines()

total = 0
for line in lines:
    total_line = count_possibilities(line)
    total += total_line

print(total)