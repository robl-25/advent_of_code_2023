from itertools import cycle


def parse_graph(lines):
    graph = {}

    for line in lines:
        node = line.split(' ')[0]
        left = line.split('(')[1].split(',')[0]
        right = line.split(', ')[1].strip(')')

        graph[node] = {'L': left, 'R': right}

    return graph


with open('day-8/part-1.txt') as f:
    lines = f.read().splitlines()

instructions = list(lines[0])

lines = lines[2:]

graph = parse_graph(lines)

current_node = 'AAA'
end_node = 'ZZZ'
steps = 0

for instruction in cycle(instructions):
    steps += 1
    current_node = graph[current_node][instruction]

    if current_node == end_node:
        break

print(steps)