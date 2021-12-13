#######################################
# --- Day 13: Transparent Origami --- #
#######################################

import AOCUtils

class Paper:
    def __init__(self, dots):
        self.dots = dots

    def fold(self, fold_direction, fold_pos):
        if fold_direction == 'x':
            folded_dots = set(dot for dot in self.dots if dot[0] > fold_pos)

            for x, y in folded_dots:
                new_x = fold_pos - (x - fold_pos)
                self.dots.add((new_x, y))
        elif fold_direction == 'y':
            folded_dots = set(dot for dot in self.dots if dot[1] > fold_pos)

            for x, y in folded_dots:
                new_y = fold_pos - (y - fold_pos)
                self.dots.add((x, new_y))
        
        self.dots -= folded_dots
        
    def __str__(self):
        max_x = max(x for x, _ in self.dots)
        max_y = max(y for _, y in self.dots)

        s = []
        for y in range(max_y+1):
            for x in range(max_x+1):
                s.append('##' if (x, y) in self.dots else '  ')
            s.append('\n')

        return ''.join(s)

#######################################

raw_instructions = AOCUtils.load_input(13)

raw_dots, raw_folds = '\n'.join(raw_instructions).split('\n\n')

dots = set(tuple(map(int, dot.split(','))) for dot in raw_dots.splitlines())

folds = []
for raw_fold in raw_folds.splitlines():
    fold_direction, fold_pos = raw_fold.split()[2].split('=')
    fold_pos = int(fold_pos)

    folds.append((fold_direction, fold_pos))

paper = Paper(dots)

for i, (fold_direction, fold_pos) in enumerate(folds):
    paper.fold(fold_direction, fold_pos)

    if i == 0:
        print(f'Part 1: {len(dots)}')

print('Part 2:')
print(paper)

AOCUtils.print_time_taken()