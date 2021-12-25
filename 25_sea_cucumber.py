################################
# --- Day 25: Sea Cucumber --- #
################################

import AOCUtils

class SeaCucumberMap:
    def __init__(self, raw_sea_cucumber_map):
        self.moves = {
            '>': lambda x, y: (x, (y+1)%self.size_y),
            'v': lambda x, y: ((x+1)%self.size_x, y)
        }

        self.size_x = len(raw_sea_cucumber_map)
        self.size_y = len(raw_sea_cucumber_map[0])

        self.sea_cucumbers = dict()
        for x in range(self.size_x):
            for y in range(self.size_y):
                if raw_sea_cucumber_map[x][y] != '.':
                    self.sea_cucumbers[(x, y)] = raw_sea_cucumber_map[x][y]

    def move(self):
        moved = False

        for sea_cucumber, nxt_fn in self.moves.items():
            update = dict()
            remove = set()

            for cur in self.sea_cucumbers:
                nxt = nxt_fn(*cur)

                if self.sea_cucumbers[cur] == sea_cucumber:
                    if nxt not in self.sea_cucumbers:
                        remove.add(cur)
                        update[nxt] = sea_cucumber

            self.sea_cucumbers.update(update)
            for i in remove: self.sea_cucumbers.pop(i)

            moved |= bool(update) or bool(remove)

        return moved

    def __repr__(self):
        s = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                cur = (x, y)

                if cur in self.sea_cucumbers:
                    c = self.sea_cucumbers[cur]
                else:
                    c = '.'

                s.append(c)
            s.append('\n')
        
        return ''.join(s)

################################

raw_sea_cucumber_map = AOCUtils.load_input(25)

sea_cucumber_map = SeaCucumberMap(raw_sea_cucumber_map)

steps = 0
while True:
    steps += 1

    # print(sea_cucumber_map)

    if not sea_cucumber_map.move():
        break

print(f'Part 1: {steps}')

AOCUtils.print_time_taken()