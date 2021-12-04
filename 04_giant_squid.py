##############################
# --- Day 4: Giant Squid --- #
##############################

import AOCUtils

class Board:
    def __init__(self, grid):
        self._win_rows = []

        for i in range(grid_size):
            self._win_rows.append(set(grid[i][j] for j in range(grid_size)))
            self._win_rows.append(set(grid[j][i] for j in range(grid_size)))

    def mark_number(self, number_drawn):
        for row in self._win_rows:
            row.discard(number_drawn)

    @property
    def has_won(self):
        return any(len(row) == 0 for row in self._win_rows)

    @property
    def unmarked_sum(self):
        # Each number is summed twice, halve the result to get the real sum
        return sum(sum(row) for row in self._win_rows) // 2

def get_win_order(boards, numbers_drawn):
    for number_drawn in numbers_drawn:
        for board in boards:
            if board.has_won: continue

            board.mark_number(number_drawn)

            if board.has_won:
                yield board.unmarked_sum * number_drawn

##############################

bingo = AOCUtils.load_input(4)
grid_size = 5

numbers_drawn = list(map(int, bingo[0].split(',')))

boards = []
for raw_board in '\n'.join(bingo[2:]).split('\n\n'):
    grid = [list(map(int, row.split())) for row in raw_board.split('\n')]
    board = Board(grid)

    boards.append(board)

win_order = list(get_win_order(boards, numbers_drawn))

print(f'Part 1: {win_order[0]}')

print(f'Part 2: {win_order[-1]}')

AOCUtils.print_time_taken()