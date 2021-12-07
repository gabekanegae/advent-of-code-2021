##########################################
# --- Day 7: The Treachery of Whales --- #
##########################################

import AOCUtils

def get_fuel_cost_cheap(crabs):
    cost_func = lambda a, b: abs(a - b)

    median = sorted(crabs)[len(crabs) // 2]

    cost = sum(cost_func(crab, median) for crab in crabs)

    return cost

def get_fuel_cost_expensive(crabs):
    cost_func = lambda a, b: abs(a - b) * (abs(a - b) + 1) // 2

    floor_mean = sum(crabs) // len(crabs)
    ceil_mean = floor_mean + 1

    floor_mean_cost = sum(cost_func(crab, floor_mean) for crab in crabs)
    ceil_mean_cost = sum(cost_func(crab, ceil_mean) for crab in crabs)

    return min(floor_mean_cost, ceil_mean_cost)

##########################################

raw_crabs = AOCUtils.load_input(7)
crabs = list(map(int, raw_crabs.split(',')))

print(f'Part 1: {get_fuel_cost_cheap(crabs)}')

print(f'Part 2: {get_fuel_cost_expensive(crabs)}')

AOCUtils.print_time_taken()