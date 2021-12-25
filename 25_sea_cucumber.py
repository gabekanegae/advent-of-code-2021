################################
# --- Day 25: Sea Cucumber --- #
################################

from copy import deepcopy
import AOCUtils

def move(state):
    new_state = deepcopy(state)
    for i in range(size_x):
        for j in range(size_y):
            if state[i][j] == '>':
                if state[i][(j+1)%size_y] == '.':
                    new_state[i][j] = '.'
                    new_state[i][(j+1)%size_y] = '>'

    state = deepcopy(new_state)
    for i in range(size_x):
        for j in range(size_y):
            if state[i][j] == 'v':
                if state[(i+1)%size_x][j] == '.':
                    new_state[i][j] = '.'
                    new_state[(i+1)%size_x][j] = 'v'

    return new_state

################################

raw_cur_map = AOCUtils.load_input(25)

cur_map = list(map(list, raw_cur_map))

size_x = len(cur_map)
size_y = len(cur_map[0])

steps = 0
while True:
    steps += 1
    start_map = deepcopy(cur_map)

    # for i in range(size_x):
    #     for j in range(size_y):
    #         print(end=cur_map[i][j])
    #     print()
    # input()
    
    cur_map =  move(cur_map)
    if cur_map == start_map:
        break

print(f'Part 1: {steps}')

AOCUtils.print_time_taken()