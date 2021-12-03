####################################
# --- Day 3: Binary Diagnostic --- #
####################################

import AOCUtils

def get_most_common_bit(report, pos, tiebreak=None):
    bits = [r[pos] for r in report]
    zeros, ones = bits.count('0'), bits.count('1')

    if ones > zeros:
        return '1'
    elif zeros > ones:
        return '0'
    else:
        return tiebreak

def get_least_common_bit(report, pos, tiebreak=None):
    most = get_most_common_bit(report, pos)
    return {'0': '1', '1': '0', None: tiebreak}[most]

def get_rating(report, bit_criteria, tiebreak):
    pos = 0

    l, r = 0, len(report)-1
    while l < r:
        keep_bit = bit_criteria(report[l:r+1], pos, tiebreak=tiebreak)

        if keep_bit == '0':
            while report[r][pos] == '1': # Discard all with 1s at pos
                r -= 1
        else:
            while report[l][pos] == '0': # Discard all with 0s at pos
                l += 1

        pos += 1

    return report[l]

####################################

length = 12

# My utils func read all lines as ints, so had to revert that
report = [str(r).zfill(length) for r in AOCUtils.load_input(3)]

gamma_rate = ''.join(get_most_common_bit(report, i) for i in range(length))
epsilon_rate = ''.join(get_least_common_bit(report, i) for i in range(length))

power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
print(f'Part 1: {power_consumption}')

report.sort()

oxygen_rating = get_rating(report, get_most_common_bit, tiebreak='1')
co2_rating = get_rating(report, get_least_common_bit, tiebreak='0')

life_support_rating = int(oxygen_rating, 2) * int(co2_rating, 2)
print(f'Part 2: {life_support_rating}')

AOCUtils.print_time_taken()