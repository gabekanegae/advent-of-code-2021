##########################################
# --- Day 7: The Treachery of Whales --- #
##########################################

import AOCUtils

def get_fuel_cost(crabs, cost_func):
    # Best goal will be the median for L1 norm and
    # between median and mean for L2 norm
    median = sorted(crabs)[len(crabs)//2]
    mean = sum(crabs) // len(crabs)

    best_cost = float('inf')
    for goal in range(min(median, mean), max(median, mean)+1):
        cost = sum(cost_func(crab, goal) for crab in crabs)
        best_cost = min(cost, best_cost)

    return best_cost

##########################################

raw_crabs = AOCUtils.load_input(7)
crabs = list(map(int, raw_crabs.split(',')))

# L1 norm
cheap = lambda a, b: abs(a - b)

print(f'Part 1: {get_fuel_cost(crabs, cheap)}')

# Triangle number, which is also the average of L1 and L2 norms
expensive = lambda a, b: abs(a - b) * (abs(a - b) + 1) // 2

print(f'Part 2: {get_fuel_cost(crabs, expensive)}')

AOCUtils.print_time_taken()

# http://www.johnmyleswhite.com/notebook/2013/03/22/modes-medians-and-means-an-unifying-perspective/
#
#   The mode minimizes the number of times that one of the numbers in our
#   summarized list is not equal to the summary that we use.
#     argmin_s @ sum_i |x_i - s|^0
#   The median minimizes the average distance between each number and our summary.
#     argmin_s @ sum_i |x_i - s|^1
#   The mean minimizes the average squared distance between each number and our summary.
#     argmin_s @ sum_i x_i - s|^2