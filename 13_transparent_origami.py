#######################################
# --- Day 13: Transparent Origami --- #
#######################################

import AOCUtils

def print_paper(dots):
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    for y in range(max_y+1):
        for x in range(max_x+1):
            print('##' if (x, y) in dots else '  ', end='')
        print('')

#######################################

raw_instructions = AOCUtils.load_input(13)

raw_dots, raw_folds = '\n'.join(raw_instructions).split('\n\n')

dots = set(tuple(map(int, dot.split(','))) for dot in raw_dots.splitlines())

folds = []
for raw_fold in raw_folds.splitlines():
    fold_direction, fold_pos = raw_fold.split()[2].split('=')
    fold_pos = int(fold_pos)

    folds.append((fold_direction, fold_pos))

part_1_complete = False
for fold_direction, fold_pos in folds:
    if fold_direction == 'y':
        folded_dots = set(dot for dot in dots if dot[1] > fold_pos)
        dots -= folded_dots

        for dot_x, dot_y in folded_dots:
            new_dot = (dot_x, fold_pos-(dot_y-fold_pos))
            dots.add(new_dot)
    elif fold_direction == 'x':
        folded_dots = set(dot for dot in dots if dot[0] > fold_pos)
        dots -= folded_dots

        for dot_x, dot_y in folded_dots:
            new_dot = (fold_pos-(dot_x-fold_pos), dot_y)
            dots.add(new_dot)

    if not part_1_complete:
        print(f'Part 1: {len(dots)}')
        part_1_complete = True

print('Part 2:')
print_paper(dots)

AOCUtils.print_time_taken()