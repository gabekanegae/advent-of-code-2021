#######################################
# --- Day 5: Hydrothermal Venture --- #
#######################################

from collections import defaultdict
import AOCUtils

def get_overlap_count(vents, part_two=False):
    grid = defaultdict(int)

    for start, end in vents:
        delta = None
        if start[0] == end[0]:
            delta = (0, 1)
        elif start[1] == end[1]:
            delta = (1, 0)
        elif part_two:
            if start[1] < end[1]:
                delta = (1, 1)
            else:
                delta = (1, -1)

        if delta is None: continue

        pos = start
        grid[pos] += 1

        while pos != end:
            pos = (pos[0]+delta[0], pos[1]+delta[1])
            grid[pos] += 1

    return sum(v > 1 for v in grid.values())

#######################################

raw_vents = AOCUtils.load_input(5)

vents = []
for raw_vent in raw_vents:
    raw_start, raw_end = raw_vent.split(' -> ')

    start = tuple(map(int, raw_start.split(',')))
    end = tuple(map(int, raw_end.split(',')))

    vent = tuple(sorted([start, end]))

    vents.append(vent)

print(f'Part 1: {get_overlap_count(vents)}')

print(f'Part 2: {get_overlap_count(vents, part_two=True)}')

AOCUtils.print_time_taken()