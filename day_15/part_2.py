def hash(s):
    current_value = 0

    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256

    return current_value


with open('input.txt') as file:
    sequences = next(file).strip().split(',')

boxes = [{} for _ in range(256)]

for sequence in sequences:
    if '=' in sequence:
        label, value = sequence.split('=')
        value = int(value)
        boxes[hash(label)][label] = value
    else:
        label = sequence.strip('-')
        label_hash = hash(label)

        if label in boxes[label_hash]:
            del boxes[label_hash][label]

total = 0
for i, box in enumerate(boxes):
    total += sum((i + 1) * (item_idx + 1) * v for item_idx, (k, v) in enumerate(box.items()))

print(total)