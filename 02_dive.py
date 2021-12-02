########################
# --- Day 2: Dive! --- #
########################

import AOCUtils

########################

course = AOCUtils.loadInput(2)

pos, depth = 0, 0
for step in course:
    direction, delta = step.split()
    delta = int(delta)
    
    if direction == 'forward':
        pos += delta
    elif direction == 'down':
        depth += delta
    elif direction == 'up':
        depth -= delta

ans = pos * depth
print(f'Part 1: {ans}')

pos, depth, aim = 0, 0, 0
for step in course:
    direction, delta = step.split()
    delta = int(delta)

    if direction == 'forward':
        pos += delta
        depth += aim * delta
    elif direction == 'down':
        aim += delta
    elif direction == 'up':
        aim -= delta

ans = pos * depth
print(f'Part 2: {ans}')

AOCUtils.printTimeTaken()