from itertools import islice


def up(coords):
    return (coords[0] - 1, coords[1])


def down(coords):
    return (coords[0] + 1, coords[1])


def right(coords):
    return (coords[0], coords[1] + 1)


def left(coords):
    return (coords[0], coords[1] - 1)


def sliding_window(iterable, n=2):
    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)


with open('input.txt') as file:
    data = file.read().splitlines()

commands = {
    'U': up,
    'D': down,
    'L': left,
    'R': right
}

current_node = (0, 0)
visited_nodes = [(0, 0)]

for instruction in data:
    command, quantity, _ = instruction.split(' ')
    quantity = int(quantity)

    for _ in range(quantity):
        current_node = commands[command](current_node)
        visited_nodes.append(current_node)

area = 0
visited_nodes.append(visited_nodes[0])
for node_a, node_b in sliding_window(visited_nodes):
    area += node_a[0] * node_b[1]
    area -= node_a[1] * node_b[0]

visited_nodes = set(visited_nodes)

area = abs(area * 0.5)
internal_dots = area + 1 - len(visited_nodes) / 2

print(int(len(visited_nodes) + internal_dots))