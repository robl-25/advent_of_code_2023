def hash(s):
    current_value = 0

    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256

    return current_value


with open('input.txt') as file:
    sequences = next(file).strip().split(',')

print(sum(hash(s) for s in sequences))