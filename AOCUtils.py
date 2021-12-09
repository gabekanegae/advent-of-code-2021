from time import perf_counter
import os

_start_time = None

def load_input(day):
    global _start_time

    _start_time = perf_counter()

    day = str(day)
    filename = f'input{day.zfill(2)}.txt'
    filepath = os.path.join('inputs', filename)

    with open(filepath) as f:
        content = [l.rstrip('\n') for l in f.readlines()]

    if len(content) == 1:
        try:
            return int(content[0])
        except:
            try:
                return [int(i) for i in content[0].split()]
            except:
                return content[0]
    else:
        try:
            return [int(i) for i in content]
        except:
            return content

def print_time_taken():
    global _start_time
    _end_time = perf_counter()
    
    delta = _end_time - _start_time
    print('Time: {:.3f}s'.format(delta))