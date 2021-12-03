####################################
# --- Day 3: Binary Diagnostic --- #
####################################

import AOCUtils

def get_most_common_bit(report, pos, tiebreak=None):
    zeros = [r[pos] for r in report].count('0')
    ones = [r[pos] for r in report].count('1')

    if ones > zeros:
        return '1'
    elif zeros > ones:
        return '0'
    else:
        return tiebreak

def get_least_common_bit(report, pos, tiebreak=None):
    most = get_most_common_bit(report, pos)
    return {'0': '1', '1': '0', None: tiebreak}[most]

####################################

length = 12
report = [str(r).zfill(length) for r in AOCUtils.load_input(3)]

gamma = ''.join(get_most_common_bit(report, i) for i in range(length))
epsilon = ''.join({'0': '1', '1': '0'}[i] for i in gamma)

power_consumption = int(gamma, 2) * int(epsilon, 2)
print(f'Part 1: {power_consumption}')

report.sort()

pos = 0
l, r = 0, len(report)-1
while l < r:
    most_common = get_most_common_bit(report[l:r+1], pos, tiebreak='1')
    if most_common == '0':
        while report[r][pos] == '1':
            r -= 1
    else:
        while report[l][pos] == '0':
            l += 1
    pos += 1
oxygen = report[l]

pos = 0
l, r = 0, len(report)-1
while l < r:
    least_common = get_least_common_bit(report[l:r+1], pos, tiebreak='0')
    if least_common == '0':
        while report[r][pos] == '1':
            r -= 1
    else:
        while report[l][pos] == '0':
            l += 1
    pos += 1
co2 = report[l]

life_support = int(oxygen, 2) * int(co2, 2)
print(f'Part 2: {life_support}')

AOCUtils.print_time_taken()