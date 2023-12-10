from pprint import pp
from itertools import chain
from itertools import zip_longest
import threading

def parse_maps(lines):
    maps = []
    current_map = None

    for line in lines:
        # Header
        if line.endswith('map:'):
            continue

        if not line:
            maps.append(current_map)
            current_map = None
        else:
            if current_map is None:
                current_map = []

            [dst_range_start, src_range_start, length] = [int(i) for i in line.split()]

            src_range = range(src_range_start, src_range_start + length)
            dst_range = range(dst_range_start, dst_range_start + length)

            current_map.append([src_range, dst_range])


    maps.append(current_map)

    return maps


def seed_value(seed, maps):
    item = seed

    for idx, map in enumerate(maps):
        current_item = item

        for src_range, dst_range in map:
            if current_item in src_range:
                item = dst_range.start + (item - src_range.start)
                break

    return item


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


with open('day-5/part-2.txt') as f:
    lines = f.read().splitlines()

lines = iter(lines)

seeds = []
total_length = 0
for start, length in grouper([int(i) for i in next(lines).split(' ')[1:]], 2):
    seeds.append(range(start, start + length))
    total_length += length

next(lines)
maps = parse_maps(lines)
min_seed_value = -1
current_index = 0

for seed in chain(*seeds):
    print(f'Proccessed: {((current_index/total_length) * 100):.3f}%', end='\r')
    location = seed_value(seed, maps)
    current_index += 1

    if min_seed_value == -1:
        min_seed_value = location
    elif min_seed_value > location:
        min_seed_value = location

print()
print(min_seed_value)
