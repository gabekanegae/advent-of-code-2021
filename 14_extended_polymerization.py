###########################################
# --- Day 14: Extended Polymerization --- #
###########################################

from collections import defaultdict
import AOCUtils

def polymerize(template, rules, steps):
    element_freq = defaultdict(int)
    for elem in template:
        element_freq[elem] += 1

    pair_freq = defaultdict(int)
    for pair in (a+b for a, b in zip(template, template[1:])):
        pair_freq[pair] += 1

    for _ in range(steps):
        for pair, freq in list(pair_freq.items()):
            if pair not in rules: continue
            new = rules[pair]

            pair_freq[pair] -= freq
            pair_freq[pair[0]+new] += freq
            pair_freq[new+pair[1]] += freq

            element_freq[new] += freq

    freqs = element_freq.values()
    return max(freqs) - min(freqs)

###########################################

formula = AOCUtils.load_input(14)

template = formula[0]

raw_rules = [r.split(' -> ') for r in formula[2:]]
rules = {k: v for k, v in raw_rules}

print(f'Part 1: {polymerize(template, rules, 10)}')

print(f'Part 2: {polymerize(template, rules, 40)}')

AOCUtils.print_time_taken()