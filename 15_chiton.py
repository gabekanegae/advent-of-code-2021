##########################
# --- Day 15: Chiton --- #
##########################

from heapq import heappush, heappop
import AOCUtils

def dijkstra(cave, cave_size, start, end):
    costs = dict()

    heap = [(0, start)]
    while heap:
        cost, cur = heappop(heap)

        if cur == end:
            return cost

        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            nxt = (cur[0] + dx, cur[1] + dy)
            if not (0 <= nxt[0] < cave_size and 0 <= nxt[1] < cave_size):
                continue

            nxt_cost = cost + cave[nxt[0]][nxt[1]]

            if nxt in costs and costs[nxt] <= nxt_cost:
                continue

            costs[nxt] = nxt_cost
            heappush(heap, (nxt_cost, nxt))

##########################

cave_size = 100

# My utils func read all lines as ints, so had to revert that
cave = [list(map(int, str(r).zfill(cave_size))) for r in AOCUtils.load_input(15)]

start = (0, 0)
end = (cave_size-1, cave_size-1)

print(f'Part 1: {dijkstra(cave, cave_size, start, end)}')

multiplier = 5

new_cave_size = cave_size * multiplier

new_start = start
new_end = (new_cave_size-1, new_cave_size-1)

new_cave = [[None for _ in range(new_cave_size)] for _ in range(new_cave_size)]
for tile_x in range(multiplier):
    for tile_y in range(multiplier):
        for i in range(cave_size):
            for j in range(cave_size):
                new_risk_level = (cave[i][j] + tile_x + tile_y - 1) % 9 + 1
                
                new_i = tile_x * cave_size + i
                new_j = tile_y * cave_size + j
                new_cave[new_i][new_j] = new_risk_level

print(f'Part 2: {dijkstra(new_cave, new_cave_size, new_start, new_end)}')

AOCUtils.print_time_taken()