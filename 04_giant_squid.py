##############################
# --- Day 4: Giant Squid --- #
##############################

import AOCUtils

def get_sum_of_unmarked_numbers(board):
    total = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] != -1:
                total += board[i][j]

    return total

def get_win_order(boards, numbers_drawn):
    for number_drawn in numbers_drawn:
        for board_idx in range(len(boards)):
            if boards[board_idx] is None: continue

            for i in range(grid_size):
                for j in range(grid_size):
                    if boards[board_idx][i][j] == number_drawn:
                        boards[board_idx][i][j] = -1

            for i in range(grid_size):
                if all(boards[board_idx][i][j] == -1 for j in range(grid_size)) or \
                   all(boards[board_idx][j][i] == -1 for j in range(grid_size)):
                    yield get_sum_of_unmarked_numbers(boards[board_idx]) * number_drawn

                    boards[board_idx] = None
                    break

##############################

bingo = AOCUtils.load_input(4)
grid_size = 5

numbers_drawn = list(map(int, bingo[0].split(',')))

boards = []
for raw_board in '\n'.join(bingo[2:]).split('\n\n'):
    board = [list(map(int, row.split())) for row in raw_board.split('\n')]
    boards.append(board)

win_order = list(get_win_order(boards, numbers_drawn))

print(f'Part 1: {win_order[0]}')

print(f'Part 2: {win_order[-1]}')

AOCUtils.print_time_taken()