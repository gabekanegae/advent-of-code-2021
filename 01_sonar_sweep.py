##############################
# --- Day 1: Sonar Sweep --- #
##############################

import AOCUtils

################################

depths = AOCUtils.loadInput(1)

increases = 0
for i in range(1, len(depths)):
    if depths[i-1] < depths[i]:
        increases += 1

print(f'Part 1: {increases}')

increases = 0
for i in range(1, len(depths)-2):
    cur = depths[i-1] + depths[i] + depths[i+1]
    nxt = depths[i] + depths[i+1] + depths[i+2]
    if cur < nxt:
        increases += 1

print(f'Part 2: {increases}')

AOCUtils.printTimeTaken()