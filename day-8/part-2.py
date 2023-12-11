import math
from itertools import cycle


def parse_graph(lines):
    graph = {}

    for line in lines:
        node = line.split(' ')[0]
        left = line.split('(')[1].split(',')[0]
        right = line.split(', ')[1].strip(')')

        graph[node] = {'L': left, 'R': right}

    return graph


def cycle_size(node, graph, instructions):
    path = []

    for instruction_index, instruction in cycle(enumerate(instructions)):
        node = graph[node][instruction]
        current_node = {
            'node': node,
            'instruction': instruction_index
        }

        if current_node in path:
            break

        path.append(current_node)

    cycle_start = path.index(current_node)

    return len(path) - cycle_start


with open('day-8/part-2.txt') as f:
    lines = f.read().splitlines()

instructions = list(lines[0])

lines = lines[2:]

graph = parse_graph(lines)

starting_nodes = [k for k in graph if k.endswith('A')]

cycle_sizes = []

for idx, node in enumerate(starting_nodes):
    cycle_sizes.append(cycle_size(node, graph, instructions))
    print(f'{(idx + 1)/len(starting_nodes) * 100:.3f}%', end='\r')

print(f'{(idx + 1)/len(starting_nodes) * 100:.3f}%')

print(math.lcm(*cycle_sizes))