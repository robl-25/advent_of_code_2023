def get_numbers(line):
  digits = []

  for index, _ in enumerate(line):
    digit = is_digit(line, index)

    if digit is not None:
      digits.append(digit)

  first = digits[0]
  last = digits[-1]

  return int(first+last)

def is_digit(line, index):
  if line[index].isdigit():
    return line[index]

  numbers = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
  }

  for key, value in numbers.items():
    if line[index:(index + len(key))] == key:
      return value

  return None

with open('day-1/day-1.txt') as f:
  print(sum(get_numbers(line) for line in f))