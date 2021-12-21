#############################
# --- Day 18: Snailfish --- #
#############################

from itertools import permutations
from functools import reduce
import AOCUtils

def explode_snailfish(n):
    for i, (x, x_level) in enumerate(n[:-1]):
        if x_level < 5:
            continue

        y, _ = n[i+1]

        insert = []
        if i > 0:
            left_ele, left_level = n[i-1]
            insert.append((left_ele + x, left_level))
        insert.append((0, x_level-1))
        if i+1 < len(n)-1:
            right_ele, right_level = n[i+2]
            insert.append((right_ele + y, right_level))

        n = n[:max(0, i-1)] + insert + n[i+3:]
        return True, n

    return False, n

def split_snailfish(n):
    for i, (ele, level) in enumerate(n):
        if ele < 10: continue

        a = ele // 2
        b = ele - a

        n = n[:i] + [(a, level+1), (b, level+1)] + n[i+1:]
        return True, n

    return False, n

def reduce_snailfish(n):
    while True:
        did_something, n = explode_snailfish(n)
        if did_something: continue

        did_something, n = split_snailfish(n)
        if not did_something: break

    return n

def add_snailfish(a, b):
    return reduce_snailfish([(ele, level+1) for ele, level in a+b])

def flatten_snalfish_number(n):
    flat_number = []

    level = 0

    i = 0
    while i < len(n):
        if n[i] == '[': level += 1
        elif n[i] == ']': level -= 1
        
        j = i
        while j < len(n) and n[j].isnumeric():
            j += 1

        if j != i:
            flat_number.append((int(n[i:j]), level))

        i += 1

    return flat_number

def magnitude(n):
    to_be_done = list(reversed(n))
    stack = [to_be_done.pop()]

    while to_be_done:
        cur_ele, cur_level = to_be_done.pop()
        prev_ele, prev_level = stack.pop()

        if cur_level == prev_level:
            stack.append((3 * prev_ele + 2 * cur_ele, cur_level - 1))

            while len(stack) > 1 and stack[-1][1] == stack[-2][1]:
                cur_ele, cur_level = stack.pop()
                prev_ele, prev_level = stack.pop()

                stack.append((3 * prev_ele + 2 * cur_ele, cur_level - 1))
        else:
            stack.append((prev_ele, prev_level))
            stack.append((cur_ele, cur_level))

    return stack[0][0]

#############################

raw_snailfish_numbers = AOCUtils.load_input(18)

snailfish_numbers = list(map(flatten_snalfish_number, raw_snailfish_numbers))

final_sum = reduce(add_snailfish, snailfish_numbers)

final_magnitude = magnitude(final_sum)
print(f'Part 1: \'{final_magnitude}\'')

max_magnitude = max(magnitude(add_snailfish(a, b)) for a, b in permutations(snailfish_numbers, 2))
print(f'Part 2: \'{max_magnitude}\'')

AOCUtils.print_time_taken()