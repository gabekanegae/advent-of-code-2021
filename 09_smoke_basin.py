##############################
# --- Day 9: Smoke Basin --- #
##############################

from collections import deque
import AOCUtils

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_low_points(cave):
    low_points = []
    for x in range(cave_size_x):
        for y in range(cave_size_y):
            higher_neighbors_amt = 0
            for dx, dy in directions:
                nxt_x, nxt_y = x + dx, y + dy

                # Count OOB as higher neighbor as well
                if not (0 <= nxt_x < cave_size_x and 0 <= nxt_y < cave_size_y):
                   higher_neighbors_amt += 1
                elif cave[nxt_x][nxt_y] > cave[x][y]:
                    higher_neighbors_amt += 1

            if higher_neighbors_amt == len(directions):
                low_points.append((x, y))

    return low_points

def get_basin_sizes(cave, low_points):
    basin_sizes = []

    for low_point in low_points:
        queue = deque([low_point])
        visited = set()
        while queue:
            x, y = queue.popleft()

            if (x, y) in visited: continue
            visited.add((x, y))

            for dx, dy in directions:
                nxt_x, nxt_y = x + dx, y + dy

                # Skip if OOB
                if not (0 <= nxt_x < cave_size_x and 0 <= nxt_y < cave_size_y): continue

                # Skip if not higher than current
                if not (cave[nxt_x][nxt_y] > cave[x][y]): continue

                # Skip 9s
                if cave[nxt_x][nxt_y] == 9: continue

                queue.append((nxt_x, nxt_y))

        basin_size = len(visited)
        basin_sizes.append(basin_size)

    return basin_sizes

##############################

cave_size_y = 100

# My utils func read all lines as ints, so had to revert that
cave = [list(map(int, str(r).zfill(cave_size_y))) for r in AOCUtils.load_input(9)]

cave_size_x = len(cave)
low_points = get_low_points(cave)

risk_levels = sum(cave[i][j] for i, j in low_points) + len(low_points)
print(f'Part 1: {risk_levels}')

basins = sorted(get_basin_sizes(cave, low_points), reverse=True)

p2 = basins[0] * basins[1] * basins[2]
print(f'Part 2: {p2}')

AOCUtils.print_time_taken()