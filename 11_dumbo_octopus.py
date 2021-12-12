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
    for i in range(grid_size):
        for j in range(grid_size):
            grid[i][j] += 1

    while True:
        has_changes = False
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] > 9:
                    has_changes = True
                    for dx, dy in mov8:
                        new_x, new_y = i + dx, j + dy
                        if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
                            continue

                        grid[new_x][new_y] += 1
                    grid[i][j] = float('-inf')

        if not has_changes: break

    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] < 0:
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