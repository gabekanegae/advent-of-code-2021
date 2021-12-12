#################################
# --- Day 11: Dumbo Octopus --- #
#################################

import AOCUtils

mov8 = [
    (-1, -1), (-1, 0), (-1, 1),
     (0, -1),           (0, 1),
     (1, -1),  (1, 0),  (1, 1)
    ]

def update(grid):
    will_flash = set()
    has_flashed = set()

    for i in range(grid_size):
        for j in range(grid_size):
            grid[i][j] += 1
            if grid[i][j] > 9:
                will_flash.add((i, j))

    while will_flash:
        flash_x, flash_y = will_flash.pop()
        has_flashed.add((flash_x, flash_y))

        for dx, dy in mov8:
            new_x, new_y = flash_x + dx, flash_y + dy
            if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
                continue

            if (new_x, new_y) in has_flashed:
                continue

            grid[new_x][new_y] += 1
            if grid[new_x][new_y] > 9:
                will_flash.add((new_x, new_y))

    for (i, j) in has_flashed:
        grid[i][j] = 0

#################################

grid_size = 10

# My utils func read all lines as ints, so had to revert that
grid = [list(map(int, str(r).zfill(grid_size))) for r in AOCUtils.load_input(11)]

total_flashes = 0
for _ in range(100):
    update(grid)

    flashes = sum(row.count(0) for row in grid)
    total_flashes += flashes

print(f'Part 1: {total_flashes}')

step = 100
while True:
    step += 1
    update(grid)

    flashes = sum(row.count(0) for row in grid)
    if flashes == grid_size * grid_size:
        break

print(f'Part 2: {step}')

AOCUtils.print_time_taken()