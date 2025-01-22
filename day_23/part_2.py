from dataclasses import dataclass
from dataclasses import field
from collections import deque


@dataclass
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    visited: bool=False
    distance: int=float('inf')

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    # Gets neighbor in `self.matrix` given a `direction`.
    def _neighbor(self, direction):
        neighbor_coords = (
            self.coords[0] + self.directions[direction][0],
            self.coords[1] + self.directions[direction][1]
        )

        if neighbor_coords[0] not in range(len(self.matrix)):
            return None

        if neighbor_coords[1] not in range(len(self.matrix[0])):
            return None

        if self.matrix[neighbor_coords[0]][neighbor_coords[1]].symbol == '#':
            return None

        return self.matrix[neighbor_coords[0]][neighbor_coords[1]]

    # All neighbors in `self.directions`.
    def neighbors(self):
        return {self._neighbor(direction) for direction in self.directions if self._neighbor(direction) is not None}

    # Makes nodes equal if they have the same `coords`.
    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.distance < other.distance

    def __hash__(self):
        return hash(self.coords)

    def reset(self):
        self.visited = False
        self.distance = float('inf')


def reset(matrix):
    for _, n in enumerate_n(matrix, n=2):
        n.reset()


def enumerate_n(iterable, start=0, n=1):
    from collections.abc import Iterable

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


def backtrack(current_node, target, nodes, distance=0):
    if current_node == target:
        return distance

    distances = []

    for step, neighbor in nodes[current_node]:
        if neighbor.visited:
            continue

        neighbor.visited = True
        distances.append(backtrack(neighbor, target, nodes, distance + step))
        neighbor.visited = False

    return max(distances, default=-1)


def dijkstra(start, target_nodes):
    import heapq

    start.distance = 0

    nodes = [start]
    heapq.heapify(nodes)

    while nodes:
        # Get node with smallest distance
        node = heapq.heappop(nodes)

        if node.visited:
            continue

        # Mark current node as visited in current direction
        node.visited = True

        # Optionally stop search when we reach the given `target_node`
        if node != start and node in target_nodes:
            continue

        for neighbor in node.neighbors():
            if neighbor.symbol == '#':
                continue

            neighbor.distance = min(neighbor.distance, node.distance + 1)

            if not neighbor.visited:
                heapq.heappush(nodes, neighbor)


def bifurcation_nodes(matrix):
    return [node for _, node in enumerate_n(matrix, n=2) if len(node.neighbors()) > 2 and node.symbol != '#']


with open('input.txt') as f:
    matrix = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

start = next(node for node in matrix[0] if node.symbol == '.')
end = next(node for node in matrix[-1] if node.symbol == '.')

bifurcations = [start, end, *bifurcation_nodes(matrix)]
reduced_graph_nodes = deque(bifurcations.copy())

nodes = {}

while reduced_graph_nodes:
    current_node = reduced_graph_nodes.popleft()

    dijkstra(current_node, bifurcations)

    nodes[current_node] = [(n.distance, n) for n in bifurcations if n.distance not in {float('inf'), 0}]

    reset(matrix)

print(backtrack(start, end, nodes))
