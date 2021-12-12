#################################
# --- Day 11: Dumbo Octopus --- #
#################################

import AOCUtils

mov8 = [
    (-1, -1), (-1, 0), (-1, 1),
     (0, -1),           (0, 1),
     (1, -1),  (1, 0),  (1, 1)
    ]

class OctopusGrid:
    def __init__(self, grid):
        self.grid = grid

    def update(self):
        will_flash = set()
        has_flashed = set()

        for i in range(len(grid)):
            for j in range(len(grid)):
                self.grid[i][j] += 1
                if self.grid[i][j] > 9:
                    will_flash.add((i, j))

        while will_flash:
            flash_x, flash_y = will_flash.pop()
            has_flashed.add((flash_x, flash_y))

            for dx, dy in mov8:
                new_x, new_y = flash_x + dx, flash_y + dy
                if not (0 <= new_x < len(grid) and 0 <= new_y < len(grid)):
                    continue

                if (new_x, new_y) in has_flashed:
                    continue

                grid[new_x][new_y] += 1
                if grid[new_x][new_y] > 9:
                    will_flash.add((new_x, new_y))

        for (i, j) in has_flashed:
            self.grid[i][j] = 0

    @property
    def current_flashes(self):
        return sum(row.count(0) for row in self.grid)

    @property
    def all_flashing(self):
        return self.current_flashes == len(grid) * len(grid)

#################################

grid_size = 10

# My utils func read all lines as ints, so had to revert that
grid = [list(map(int, str(r).zfill(grid_size))) for r in AOCUtils.load_input(11)]

octopus_grid = OctopusGrid(grid)
step = 0

total_flashes = 0
for _ in range(100):
    octopus_grid.update()
    step += 1

    total_flashes += octopus_grid.current_flashes

print(f'Part 1: {total_flashes}')

while not octopus_grid.all_flashing:
    octopus_grid.update()
    step += 1

print(f'Part 2: {step}')

AOCUtils.print_time_taken()