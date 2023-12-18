from heapq import heappush, heappop


def is_inside(coords, matrix):
    row, col = coords

    row_range = range(len(matrix))
    col_range = range(len(matrix[0]))

    return row in row_range and col in col_range


def add_on_queue(matrix, next_steps, heat_loss, current_coords, direction, steps = 1):
    new_row = current_coords[0] + direction[0]
    new_col = current_coords[1] + direction[1]

    new_coords = (new_row, new_col)

    if not is_inside(new_coords, matrix):
        return
    
    heappush(
        next_steps, 
        (heat_loss + matrix[new_row][new_col], new_coords, direction, steps)
    )


def all_possibles_directions():
    return [(1, 0), (0, 1), (-1, 0), (0, -1)]


def min_loss(matrix):
    visited = set()
    next_steps = [(0, (0,0), (0,0), 0)]
    target_coords = (len(matrix) - 1, len(matrix[0]) - 1)

    while next_steps:
        heat_loss, current_coords, direction, steps = heappop(next_steps)

        if current_coords == target_coords:
            break
        
        if (current_coords, direction, steps) in visited:
            continue
        
        visited.add((current_coords, direction, steps))

        if direction != (0, 0) and steps < 3:
            add_on_queue(matrix, next_steps, heat_loss, current_coords, direction, steps + 1)

        for new_direction in all_possibles_directions():
            if new_direction != direction and new_direction != (-direction[0], -direction[1]):
                add_on_queue(matrix, next_steps, heat_loss, current_coords, new_direction)

    return heat_loss


with open('input.txt') as file:
    matrix = []

    for line in file.read().splitlines():
        l = [int(item) for item in line]
        matrix.append(l)

min_heat_loss = min_loss(matrix)

print(min_heat_loss)