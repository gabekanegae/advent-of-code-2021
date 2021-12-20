##############################
# --- Day 20: Trench Map --- #
##############################

import AOCUtils

mov9 = [
    (-1, -1), (-1, 0), (-1, 1),
     (0, -1),  (0, 0),  (0, 1),
     (1, -1),  (1, 0),  (1, 1)
    ]

def invert_image(image):
    px = [i[0] for i in image]
    py = [i[1] for i in image]
    min_x, max_x = min(px), max(px)
    min_y, max_y = min(py), max(py)

    inverted_image = set()    
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if (x, y) not in image:
                inverted_image.add((x, y))

    return inverted_image

def invert_enhancement(enhancement):
    return ''.join(reversed(enhancement))

def enhance_once(image, enhancement):
    px = [i[0] for i in image]
    py = [i[1] for i in image]
    min_x, max_x = min(px), max(px)
    min_y, max_y = min(py), max(py)

    new_image = set()
    for x in range(min_x-1, max_x+1+1):
        for y in range(min_y-1, max_y+1+1):
            s = ''.join(str(int((x+dx, y+dy) in image)) for dx, dy in mov9)
            idx = int(s, 2)

            if enhancement[idx] == '#':
                new_image.add((x,y))

    return new_image

def enhance(image, enhancement, iterations):
    assert iterations % 2 == 0

    for i in range(iterations//2):
        image = enhance_once(image, enhancement)
        image = enhance_once(invert_image(image), invert_enhancement(enhancement))

    return len(image)

##############################

raw_data = AOCUtils.load_input(20)

enhancement = raw_data[0]
raw_image = raw_data[2:]

# assert enhancement[0] == '#' and enhancement[511] == '.'

size_x, size_y = len(raw_image), len(raw_image[0])

image = set()
for x in range(size_x):
    for y in range(size_y):
        if raw_image[x][y] == '#':
            image.add((x, y))

print(f'Part 1: {enhance(image, enhancement, 2)}')

print(f'Part 2: {enhance(image, enhancement, 50)}')

AOCUtils.print_time_taken()