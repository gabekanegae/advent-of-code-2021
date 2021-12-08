#######################################
# --- Day 8: Seven Segment Search --- #
#######################################

import AOCUtils

def decode(entry_in, entry_out):
    mapping = dict()

    # [1, 4, 7, 8]: can be determined instantly by their segment amount
    easy_mapping = {1: 2, 4: 4, 7: 3, 8: 7}
    for n, seg_amt in easy_mapping.items():
        mapping[n] = next(s for s in entry_in if len(s) == seg_amt)

    # Group the ones left by segment amount
    possible_0_6_9 = set(s for s in entry_in if len(s) == 6)
    possible_2_3_5 = set(s for s in entry_in if len(s) == 5)

    # [0, 6, 9]: only 6 isn't a superset of 7
    mapping[6] = next(s for s in possible_0_6_9 if not s > mapping[7])
    possible_0_9 = possible_0_6_9 - {mapping[6]}

    # [0, 9]: only 9 is a superset of 4 - 7
    mapping[9] = next(s for s in possible_0_9 if s > mapping[4] - mapping[7])
    mapping[0] = (possible_0_9 - {mapping[9]}).pop()

    # [2, 3, 5]: only 5 is a subset of 6
    mapping[5] = next(s for s in possible_2_3_5 if s < mapping[6])
    possible_2_3 = possible_2_3_5 - {mapping[5]}

    # [2, 3]: only 3 is a subset of 9
    mapping[3] = next(s for s in possible_2_3 if s < mapping[9])
    mapping[2] = (possible_2_3 - {mapping[3]}).pop()

    reverse_mapping = {v: k for k, v in mapping.items()}

    return ''.join(str(reverse_mapping[c]) for c in entry_out)

#######################################

raw_entries = AOCUtils.load_input(8)

entries = []
for raw_entry in raw_entries:
    raw_entry_in, raw_entry_out = raw_entry.split(' | ')

    entry_in = tuple(frozenset(s) for s in raw_entry_in.split())
    entry_out = tuple(frozenset(s) for s in raw_entry_out.split())

    entries.append((entry_in, entry_out))

decoded_entries = [decode(entry_in, entry_out) for entry_in, entry_out in entries]

p1 = sum(''.join(decoded_entries).count(i) for i in '1478')
print(f'Part 1: {p1}')

p2 = sum(int(decoded_entry) for decoded_entry in decoded_entries)
print(f'Part 2: {p2}')

AOCUtils.print_time_taken()