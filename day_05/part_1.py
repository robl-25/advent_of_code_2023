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

    return item


with open('input.txt') as f:
    lines = f.read().splitlines()

lines = iter(lines)

seeds = [int(i) for i in next(lines).split(' ')[1:]]

next(lines)
maps = parse_maps(lines)
min_seed_value = min(seed_value(seed, maps) for seed in seeds)

print(min_seed_value)
