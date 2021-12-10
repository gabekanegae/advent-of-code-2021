##################################
# --- Day 10: Syntax Scoring --- #
##################################

import AOCUtils

chunk_open = {'(': ')', '[': ']', '{': '}', '<': '>'}
chunk_close = {v: k for k, v in chunk_open.items()}

syntax_error_score_table = {')': 3, ']': 57, '}': 1197, '>': 25137}

def get_syntax_error_score(line):
    stack = []
    for c in line:
        if c in chunk_open:
            stack.append(c)
        elif c in chunk_close:
            if stack.pop() != chunk_close[c]:
                return syntax_error_score_table[c]

    return 0

autocomplete_score_table = {')': 1, ']': 2, '}': 3, '>': 4}

def get_autocomplete_score(line):
    stack = []
    for c in line:
        if c in chunk_open:
            stack.append(c)
        elif c in chunk_close:
            if stack[-1] == chunk_close[c]:
                stack.pop()

    score = 0
    for c in (chunk_open[c] for c in reversed(stack)):
        score = score * 5 + autocomplete_score_table[c]
    return score

##################################

lines = AOCUtils.load_input(10)

lines_and_syntax_scores = [(line, get_syntax_error_score(line)) for line in lines]

p1 = sum(score for _, score in lines_and_syntax_scores)
print(f'Part 1: {p1}')

incomplete_lines = [line for line, score in lines_and_syntax_scores if score == 0]

autocomplete_scores = list(map(get_autocomplete_score, incomplete_lines))
autocomplete_scores.sort()

p2 = autocomplete_scores[len(autocomplete_scores)//2]
print(f'Part 2: {p2}')

AOCUtils.print_time_taken()