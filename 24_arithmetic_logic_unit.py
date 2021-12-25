#########################################
# --- Day 24: Arithmetic Logic Unit --- #
#########################################

import AOCUtils

def find_valid_model_number(relevant_values, goal_fn):
    digits = [0 for _ in relevant_values]
    digit_range = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Each instruction block (starting with `inp w`) is simply:
    # z //= A
    # if z % 26 + B != w:
    #     z = 26 * z + w + C

    # This can be converted to this stack-based iteration
    # that calculates the digits in O(digits) time
    stack = []
    for cur_idx, (A, B, C) in enumerate(relevant_values):
        if B >= 10:
            stack.append((cur_idx, C))
            continue

        prev_idx, prev_C = stack.pop()
        
        offset = prev_C + B

        best_n = goal_fn(n for n in digit_range if n+offset in digit_range)

        digits[prev_idx] = best_n
        digits[cur_idx] = best_n + offset

    return int(''.join(map(str, digits)))

#########################################

instructions = AOCUtils.load_input(24)

# There are 14 similar instruction blocks, only differing by three values, so
# keep only these, as assumptions can be made about the rest of the input
relevant_values = []
for block in ' '.join(instructions).split('inp w')[1:]:
    block = block.strip().split()

    values = [block[11], block[14], block[44]]
    relevant_values.append(list(map(int, values)))

print(f'Part 1: {find_valid_model_number(relevant_values, max)}')

print(f'Part 2: {find_valid_model_number(relevant_values, min)}')

AOCUtils.print_time_taken()