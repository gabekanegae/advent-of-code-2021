import AOCUtils

inp = AOCUtils.load_input(18)

def list_to_str(s):
    return str(s).replace(' ', '')

def str_to_list(s):
    return eval(s)

def sum_with_left_nr(n, i, tosum):
    while i >= 0 and n[i] not in '0123456789':
        i -= 1
    
    if i < 0: return n

    s = i
    while s >= 0 and n[s] in '0123456789':
        s -= 1

    if s < 0: return n

    s += 1

    # print(' left', n)
    nn = n[:s] + str(int(n[s:i+1])+tosum) + n[i+1:]
    # print(' l>  ', nn)
    return nn

def sum_with_right_nr(n, i, tosum):
    while i < len(n) and n[i] not in '0123456789':
        i += 1
    
    if i >= len(n): return n

    s = i
    while s < len(n) and n[s] in '0123456789':
        s += 1

    if s >= len(n): return n

    s -=1

    # print(' right', n)
    nn = n[:i] + str(int(n[i:s+1])+tosum) + n[s+1:]
    # print(' r>   ', nn)
    return nn

def explode(n):
    # n is list of lists
    n = list_to_str(n)
    old_n = n

    i = 0
    level = 0
    while i < len(n):
        if n[i] == '[':
            level += 1
        elif n[i] == ']':
            level -= 1

        if level == 5:
            ci = i
            while n[ci] != ']':
                ci += 1

            pair_bounds = (i, ci+1)
            pair = eval(n[pair_bounds[0]:pair_bounds[1]])
            
            # print('expl', n)
            nn = n[:i] + '0' + n[ci+1:]

            l_before = len(nn)
            nn = sum_with_left_nr(nn, i-1, pair[0])
            l_after = len(nn)
            xn = int(l_before!=l_after)
            nn = sum_with_right_nr(nn, i+1+xn, pair[1])
            # print('    ', nn)

            n =nn
            return True, eval(n)

        i += 1

    return False, eval(n)
    # n should be returned as list of lists

def split(n):
    # n is list of lists
    n = list_to_str(n)

    i = 0
    while i < len(n)-1:
        # print(n[i], n[i+1], n[i].isalnum() and n[i+1].isalnum())
        if n[i].isalnum() and n[i+1].isalnum():
            a = int(n[i:i+2])
            c = [a//2, a-(a//2)]
            # print('split', n)
            nn = n[:i] + list_to_str(c) + n[i+2:]
            # print('     ', nn)
            return True, nn
        i += 1

    return False, eval(n)

def reduce(n):
    while True:
        did_stuff, n = explode(n)
        if did_stuff: continue

        did_stuff, n = split(n)
        if not did_stuff:
            break

    return n

def add(a,b):
    c = [a, b]
    return reduce(c)

def mag(val):
    if isinstance(val, int): return val
    return 3 * mag(val[0]) + 2 * mag(val[1])

######################################################
ans = 0

inpx = []
for l in inp:
    inpx.append(eval(l))

val = inpx[0]
for v in inpx[1:]:
    val = add(val, v)

ans = mag(val)
print(f'Part 1: \'{ans}\'')

from itertools import permutations

best = -1
for a, b in permutations(inpx, 2):
    m = mag(add(a,b))
    best = max(best, m)

ans=best

print(f'Part 2: \'{ans}\'')

AOCUtils.print_time_taken()