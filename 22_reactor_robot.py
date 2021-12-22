#################################
# --- Day 22: Reactor Robot --- #
#################################

from collections import defaultdict, namedtuple
import AOCUtils

Cuboid = namedtuple('Cuboid', ['x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max'])

def intersection(a, b):
    # https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection
    x_intersect = a.x_min <= b.x_max and b.x_min <= a.x_max
    y_intersect = a.y_min <= b.y_max and b.y_min <= a.y_max
    z_intersect = a.z_min <= b.z_max and b.z_min <= a.z_max

    intersect = x_intersect and y_intersect and z_intersect
    if intersect:
        x_range = max(a.x_min, b.x_min), min(a.x_max, b.x_max)
        y_range = max(a.y_min, b.y_min), min(a.y_max, b.y_max)
        z_range = max(a.z_min, b.z_min), min(a.z_max, b.z_max)
        
        return Cuboid(*x_range, *y_range, *z_range)

    return None

def count_cubes_on(steps):
    # Keep dict of {cuboid: count} per the inclusion–exclusion principle
    cuboids = defaultdict(int)
    for state, *bounds in steps:
        new_region = Cuboid(*bounds)

        for existing_region in list(cuboids.keys()):
            intersecting_region = intersection(new_region, existing_region)

            # Cancel out the existing region
            if intersecting_region:
                cuboids[intersecting_region] -= cuboids[existing_region]

        if state == 'on':
            cuboids[new_region] += 1

    cubes_on = 0
    for cuboid, count in cuboids.items():
        x_length = (cuboid.x_max - cuboid.x_min + 1)
        y_length = (cuboid.y_max - cuboid.y_min + 1)
        z_length = (cuboid.z_max - cuboid.z_min + 1)
        volume = x_length * y_length * z_length

        cubes_on += volume * count

    return cubes_on

#################################

raw_steps = AOCUtils.load_input(22)

steps = []
for raw_step in raw_steps:
    step, raw_ranges = raw_step.split()

    x_range, y_range, z_range = [map(int, s[2:].split('..')) for s in raw_ranges.split(',')]

    step = tuple([step, *x_range, *y_range, *z_range])
    steps.append(step)

init_steps = [step for step in steps if all(abs(c) <= 50 for c in step[1:])]

print(f'Part 1: {count_cubes_on(init_steps)}')

print(f'Part 2: {count_cubes_on(steps)}')

AOCUtils.print_time_taken()