###################################
# --- Day 12: Passage Pathing --- #
###################################

from collections import deque, defaultdict
import AOCUtils

def get_path_count_1(cave_edges):
    path_count = [0]
    visited = set()

    def dfs(cur):
        if cur.islower():
            if cur in visited: return
            visited.add(cur)

        if cur == 'end':
            path_count[0] += 1
            visited.remove('end')
            return

        for neighbor in cave_edges[cur]:
            dfs(neighbor)

        if cur.islower():
            visited.remove(cur)

    dfs('start')
    return path_count[0]

def get_path_count_2(cave_edges):
    path_count = [0]
    visited = defaultdict(int)

    def dfs(cur, small_revisited=False):
        if cur.islower():
            if cur in visited:
                if cur == 'start' or small_revisited:
                    return
                else:
                    small_revisited = True

            visited[cur] += 1

        if cur == 'end':
            path_count[0] += 1
            visited.pop('end')
            return

        for neighbor in cave_edges[cur]:
            dfs(neighbor, small_revisited)

        if cur.islower():
            visited[cur] -= 1
            if visited[cur] == 0: visited.pop(cur)

    dfs('start')
    return path_count[0]

###################################

raw_cave_edges = AOCUtils.load_input(12)

cave_edges = defaultdict(list)
for raw_cave_edge in raw_cave_edges:
    a, b = raw_cave_edge.split('-')

    cave_edges[a].append(b)
    cave_edges[b].append(a)

print(f'Part 1: {get_path_count_1(cave_edges)}')

print(f'Part 2: {get_path_count_2(cave_edges)}')

AOCUtils.print_time_taken()