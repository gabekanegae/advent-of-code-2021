##############################
# --- Day 6: Lanternfish --- #
##############################

from collections import deque
import AOCUtils

def get_lanternfish(timers, day):
    new_fish = deque(timers.count(i) for i in range(9))

    for _ in range(day):
        new_fish[7] += new_fish[0]
        new_fish.rotate(-1)

    return sum(new_fish)

##############################

raw_timers = AOCUtils.load_input(6)

timers = list(map(int, raw_timers.split(',')))

print(f'Part 1: {get_lanternfish(timers, 80)}')

print(f'Part 2: {get_lanternfish(timers, 256)}')

AOCUtils.print_time_taken()