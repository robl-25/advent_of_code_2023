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


def location_to_seed(location, maps, seeds):
    item = location

    for map in maps:
        current_item = item

        for src_range, dst_range in map:
            if current_item in dst_range:
                item = src_range.start + (item - dst_range.start)
                break

    for range_seed in seeds:
        if item in range_seed:
            return True

    return False

with open('input.txt') as f:
    lines = f.read().splitlines()

lines = iter(lines)

seeds = []
total_length = 0
for start, length in grouper([int(i) for i in next(lines).split(' ')[1:]], 2):
    seeds.append(range(start, start + length))
    total_length += length

next(lines)
maps = parse_maps(lines)
found_seed = False
location = 0

while (not found_seed):
    found_seed = location_to_seed(location, maps[::-1], seeds)

    if not found_seed:
        location += 1

print(location)
