##########################################
# --- Day 7: The Treachery of Whales --- #
##########################################

import AOCUtils

def get_fuel_cost(crabs, cost_func):
    best_cost = float('inf')
    for goal in range(min(crabs), max(crabs)+1):
        cost = sum(cost_func(crab, goal) for crab in crabs)
        best_cost = min(cost, best_cost)

    return best_cost

##########################################

raw_crabs = AOCUtils.load_input(7)
crabs = list(map(int, raw_crabs.split(',')))

cheap = lambda a, b: abs(a - b)

print(f'Part 1: {get_fuel_cost(crabs, cheap)}')

expensive = lambda a, b: abs(a - b) * (abs(a - b) + 1) // 2

print(f'Part 2: {get_fuel_cost(crabs, expensive)}')

AOCUtils.print_time_taken()