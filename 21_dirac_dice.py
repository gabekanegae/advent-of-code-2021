##############################
# --- Day 21: Dirac Dice --- #
##############################

import AOCUtils

memo = dict()

def play_practice_game(p1_pos, p2_pos):
    player_pos = [p1_pos, p2_pos]
    player_score = [0, 0]

    dice_rolls = 0
    while not any(p >= 1000 for p in player_score):
        for player in range(2):
            steps = 0
            for _ in range(3):
                steps += (dice_rolls % 100) + 1
                dice_rolls += 1

            player_pos[player] = ((player_pos[player] + steps - 1) % 10) + 1
            player_score[player] += player_pos[player]

    return dice_rolls * min(player_score)

roll_table_3d6 = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

def get_wins(p1_pos, p2_pos, p1_score, p2_score):
    if p1_score >= 21: return (1, 0)
    if p2_score >= 21: return (0, 1)

    state = (p1_pos, p2_pos, p1_score, p2_score)

    if state in memo:
        return memo[state]

    wins = (0, 0)
    for steps, freq in roll_table_3d6.items():
        new_p1_pos, new_p1_score = p1_pos, p1_score

        new_p1_pos = ((new_p1_pos + steps - 1) % 10) + 1
        new_p1_score += new_p1_pos

        p1_wins, p2_wins = get_wins(p2_pos, new_p1_pos, p2_score, new_p1_score)
        wins = (wins[0] + p2_wins * freq, wins[1] + p1_wins * freq)

    memo[state] = wins
    return wins

##############################

raw_start_pos = AOCUtils.load_input(21)

start_pos = tuple(int(line.split()[-1]) for line in raw_start_pos)

print(f'Part 1: {play_practice_game(start_pos[0], start_pos[1])}')

print(f'Part 2: {max(get_wins(start_pos[0], start_pos[1], 0, 0))}')

AOCUtils.print_time_taken()