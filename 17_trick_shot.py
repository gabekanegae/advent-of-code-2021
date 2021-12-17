##############################
# --- Day 17: Trick Shot --- #
##############################

import AOCUtils

def launch_probe(velocity, target):
    vx, vy = velocity
    tx, ty = target
    px, py = 0, 0

    while True:
        # Stop simulation if:
        #  Probe is falling and target is above it.
        if vy < 0 and py < ty[0]: return None
        #  vx converges to 0 and x=0 is not in target.
        if vx == 0 and not (tx[0] <= px <= tx[1]): return None
        #  vx is neg/pos and target is to the right/left.
        if (vx < 0 and px < tx[0]) or (vx > 0 and px > tx[1]): return None

        # Update position and velocity
        px += vx
        py += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        
        vy -= 1

        if tx[0] <= px <= tx[1] and ty[0] <= py <= ty[1]:
            return True

##############################

raw_target = AOCUtils.load_input(17)

target = ''.join(raw_target.split()[2:]).split(',')
target = tuple(tuple(map(int, ax[2:].split('..'))) for ax in target)

# Max height happens when max vy happens.
# Max vy is farthest edge of target, as any more than that would
#  overshoot (see v_lim_y upper bound comment below), and I am
#  always able to choose an arbitrary vx so that this holds true.
# However, if target <= y=0, the probe falls and reaches y=0
#  with y-velocity = -vy, its next step is y-velocity = -vy-1,
#  so it overshoots the target by exactly one unit.
# In that case, max_vy is [the target abs max y - 1].
max_vy = max(abs(target[1][0])-1, abs(target[1][1]))
max_y = (max_vy * (max_vy + 1)) // 2

print(f'Part 1: {max_y}')

# As vx never changes direction, it has to have
# the same sign as the start/end of target
v_lim_x = (min(0, target[0][0]), max(0, target[0][1]))
# Lower bound:
#  As vy is always decreasing:
#  If target < y=0, vy can't be lower than the bottom of target.
#  If target >= y=0, vy >= 0.
# Upper bound:
#  vy can't be higher than the target max abs y, as its trajectory
#   would overshoot the target regardless of being above/below y=0,
#   and regardless of it (potentially) reaching target when
#   rising or falling, as the y-trajectory is symmetric.
v_lim_y = (min(0, target[1][0]), max(abs(target[1][0]), abs(target[1][1])))

hits = 0

for vx in range(v_lim_x[0], v_lim_x[1]+1):
    for vy in range(v_lim_y[0], v_lim_y[1]+1):
        velocity = (vx, vy)
        max_y = launch_probe(velocity, target)

        if max_y is not None:
            hits += 1
            # print(f'({vx}, {vy}): {max_max_y} | {hits}')

print(f'Part 2: {hits}')

AOCUtils.print_time_taken()