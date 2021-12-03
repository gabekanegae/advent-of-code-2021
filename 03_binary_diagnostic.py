####################################
# --- Day 3: Binary Diagnostic --- #
####################################

import AOCUtils

def get_most_common_bit(report, pos):
    zeros = [r[pos] for r in report].count('0')
    ones = [r[pos] for r in report].count('1')

    if ones > zeros:
        return '1'
    elif zeros > ones:
        return '0'
    else:
        return None

def get_least_common_bit(report, pos):
    most = get_most_common_bit(report, pos)
    return {'0': '1', '1': '0', None: None}[most]

####################################

length = 12
report = [str(r).zfill(length) for r in AOCUtils.load_input(3)]

gamma = ''.join(get_most_common_bit(report, i) for i in range(length))
epsilon = ''.join({'0': '1', '1': '0'}[i] for i in gamma)

power_consumption = int(gamma, 2) * int(epsilon, 2)
print(f'Part 1: {power_consumption}')

report_set = set(report)
pos = 0
while len(report_set) > 1:
    most_common = get_most_common_bit(report_set, pos)
    if most_common is None:
        most_common = '1'
    
    for r in list(report_set):
        if r[pos] != most_common:
            report_set.remove(r)
    pos += 1
oxygen = report_set.pop()

report_set = set(report)
pos = 0
while len(report_set) > 1:
    least_common = get_least_common_bit(report_set, pos)
    if least_common is None:
        least_common = '0'
    
    for r in list(report_set):
        if r[pos] != least_common:
            report_set.remove(r)
    pos += 1
co2 = report_set.pop()

life_support = int(oxygen, 2) * int(co2, 2)
print(f'Part 2: {life_support}')

AOCUtils.print_time_taken()