def get_numbers(line):
  first = next(char for char in line if char.isdigit())
  last = next(char for char in line[::-1] if char.isdigit())

  return int(first+last)

with open('day-1/input.txt') as f:
  print(sum(get_numbers(line) for line in f))