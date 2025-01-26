from dataclasses import dataclass
from fractions import Fraction


def sliding_window(iterable, n=2):
    from itertools import islice

    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)


@dataclass
class Hailstone:
    position: tuple
    speed: tuple

    def __eq__(self, other):
        return self.position == other.position and self.speed == other.speed


def find_pivot(matrix, column):
        return max(((idx, item[column]) for idx, item in enumerate(matrix)), key=lambda item: item[1])


def gaussian_elimination(A, b):
  """
  Gauss elimination method [By Bottom Science].
  From: https://www.bottomscience.com/gauss-elimination-method-python/

  A - the coefficient matrix (an n x n matrix)
  b - the right-hand side column vector (an n x 1 matrix)
  """

  n = len(A)

  # Perform Gauss elimination
  for i in range(n):
    # Find the pivot element
    pivot = abs(A[i][i])
    pivot_row = i

    for j in range(i+1, n):
      if abs(A[j][i]) > pivot:
        pivot = abs(A[j][i])
        pivot_row = j

    # Swap the pivot row with the current row (if necessary)
    if pivot_row != i:
      A[i], A[pivot_row] = A[pivot_row], A[i]
      b[i], b[pivot_row] = b[pivot_row], b[i]

    # Eliminate the current variable from the other equations
    for j in range(i+1, n):
      factor = A[j][i] / A[i][i]

      for k in range(i, n):
        A[j][k] -= factor * A[i][k]

      b[j] -= factor * b[i]

  # Back-substitute to find the solution
  x = [0] * n

  for i in range(n-1, -1, -1):
    x[i] = b[i]

    for j in range(i+1, n):
      x[i] -= A[i][j] * x[j]

    x[i] /= A[i][i]
  return x


with open('input.txt') as f:
    data = f.readlines()

hailstones = []

for line in data:
    position, speed = line.strip().split('@')

    position = [Fraction(p) for p in position.split(', ')]
    speed = [Fraction(s) for s in speed.split(', ')]

    hailstones.append(
        Hailstone(
            position=tuple(position),
            speed=tuple(speed)
        )
    )

equations = []
results = []

for index, (hailstone_a, hailstone_b) in enumerate(sliding_window(hailstones)):
    if index >= 4:
        break

    speed_a_x, speed_a_y, _ = hailstone_a.speed
    speed_b_x, speed_b_y, _ = hailstone_b.speed

    position_a_x, position_a_y, _ = hailstone_a.position
    position_b_x, position_b_y, _ = hailstone_b.position

    equation = [
        speed_a_y - speed_b_y,
        speed_b_x - speed_a_x,
        position_b_y - position_a_y,
        position_a_x - position_b_x,
    ]

    result = position_b_y * speed_b_x - position_b_x * speed_b_y + position_a_x * speed_a_y - position_a_y * speed_a_x

    equations.append(equation)
    results.append(result)

stone_position_x, stone_position_y, stone_speed_x, stone_speed_y = gaussian_elimination(equations, results)

equations = []
results = []

for hailstone in hailstones[2:4]:
    _, hailstone_speed_y, hailstone_speed_z = hailstone.speed
    _, hailstone_position_y, hailstone_position_z = hailstone.position

    equation = [
        stone_speed_y - hailstone_speed_y,
        hailstone_position_y - stone_position_y,
    ]

    result = hailstone_position_y * hailstone_speed_z + hailstone_position_z * stone_speed_y - stone_position_y * hailstone_speed_z - hailstone_position_z * hailstone_speed_y

    equations.append(equation)
    results.append(result)

stone_position_z, stone_speed_z = gaussian_elimination(equations, results)

print(sum([stone_position_x, stone_position_y, stone_position_z]))
