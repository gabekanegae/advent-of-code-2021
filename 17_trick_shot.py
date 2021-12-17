##############################
# --- Day 17: Trick Shot --- #
##############################

import AOCUtils

def launch_probe(velocity, target):
    vx, vy = velocity
    tx, ty = target

    px, py = 0, 0
    max_y = float('-inf')

    while True:
        # Stop simulation if:
        #  - Probe is falling and target is above it
        if vy < 0 and py < ty[0]: return None
        #  - vx converges to 0 and x=0 is not in target
        if vx == 0 and not (tx[0] <= px <= tx[1]): return None
        #  - vx is neg/pos and target is to the right/left
        if (vx < 0 and px < tx[0]) or (vx > 0 and px > tx[1]): return None

        # Update position and velocity
        px += vx
        py += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        
        vy -= 1

        # Compute target
        max_y = max(max_y, py)

        if tx[0] <= px <= tx[1] and ty[0] <= py <= ty[1]:
            return max_y

##############################

raw_target = AOCUtils.load_input(17)

target = ''.join(raw_target.split()[2:]).split(',')
target = tuple(tuple(map(int, ax[2:].split('..'))) for ax in target)

v_lim = ((-500, 500), (-500, 500))

max_max_y = float('-inf')
hits = 0

for vx in range(v_lim[0][0], v_lim[0][1]):
    for vy in range(v_lim[1][0], v_lim[1][1]):
        velocity = (vx, vy)
        max_y = launch_probe(velocity, target)

        if max_y is not None:
            # print(f'({vx}, {vy}): {max_max_y} | {hits}')

            max_max_y = max(max_max_y, max_y)
            hits += 1

print(f'Part 1: {max_max_y}')

print(f'Part 2: {hits}')

AOCUtils.print_time_taken()