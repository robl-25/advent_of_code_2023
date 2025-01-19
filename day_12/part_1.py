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
    return [len(g) for g in group_equal(data) if g[0] == '#'] == mask


def f(data, mask, idx):
    if idx == len(data):
        if is_valid(data, mask):
            return 1

        return 0

    if data[idx] == '?':
        data[idx] = '#'
        case_1 = f(data, mask, idx + 1)

        data[idx] = '.'
        case_2 = f(data, mask, idx + 1)

        # Undo change so that other recursion branches don't break
        data[idx] = '?'

        return case_1 + case_2

    return f(data, mask, idx + 1)



def count_possibilities(line):
    data, mask = line.split(' ')

    data = list(data)
    mask = [int(i) for i in mask.split(',')]

    return f(data, mask, 0)


with open('input.txt') as file:
    lines = file.read().splitlines()

total = 0
for line in lines:
    total_line = count_possibilities(line)
    total += total_line

print(total)