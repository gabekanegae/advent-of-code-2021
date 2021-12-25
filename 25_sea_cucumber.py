################################
# --- Day 25: Sea Cucumber --- #
################################

import AOCUtils

moves = {'>': lambda x, y: (x, (y+1)%size_y),
         'v': lambda x, y: ((x+1)%size_x, y)}

################################

raw_sea_cucumbers = AOCUtils.load_input(25)

size_x = len(raw_sea_cucumbers)
size_y = len(raw_sea_cucumbers[0])

sea_cucumbers = dict()
for x in range(size_x):
    for y in range(size_y):
        if raw_sea_cucumbers[x][y] != '.':
            sea_cucumbers[(x, y)] = raw_sea_cucumbers[x][y]

steps = 0
while True:
    steps += 1
    changed = False

    for cucumber, nxt_fn in moves.items():
        update = dict()
        remove = set()

        for cur in sea_cucumbers:
            nxt = nxt_fn(*cur)

            if sea_cucumbers[cur] == cucumber:
                if nxt not in sea_cucumbers:
                    remove.add(cur)
                    update[nxt] = cucumber

        sea_cucumbers.update(update)
        for i in remove: sea_cucumbers.pop(i)

        changed |= bool(update) or bool(remove)

    # for x in range(size_x):
    #     for y in range(size_y):
    #         cur = (x, y)
    #         print(end=(sea_cucumbers[cur] if cur in sea_cucumbers else '.'))
    #     print()
    # input()

    if not changed:
        break

print(f'Part 1: {steps}')

AOCUtils.print_time_taken()