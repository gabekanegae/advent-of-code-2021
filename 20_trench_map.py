##############################
# --- Day 20: Trench Map --- #
##############################

import AOCUtils

mov9 = [
    (-1, -1), (-1, 0), (-1, 1),
     (0, -1),  (0, 0),  (0, 1),
     (1, -1),  (1, 0),  (1, 1)
    ]

# Input is 100x100, grows 1 every iteration,
# so 150x150 should handle 50 iterations
BOUNDARY = 150

def enhance_once(image, enhancement):
    px = [i[0] for i in image]
    py = [i[1] for i in image]

    min_x, max_x = min(px+[-BOUNDARY]), max(px+[BOUNDARY])
    min_y, max_y = min(py+[-BOUNDARY]), max(py+[BOUNDARY])

    new_image = set()
    for x in range(min_x-3, max_x+1+3):
        for y in range(min_y-3, max_y+1+3):
            s = ''.join(str(int((x+dx, y+dy) in image)) for dx, dy in mov9)
            idx = int(s, 2)

            if enhancement[idx] == '#':
                new_image.add((x,y))

    return new_image

def enhance(image, enhancement, iterations):
    assert iterations % 2 == 0

    for i in range(iterations//2):
        image = enhance_once(image, enhancement)
        image = enhance_once(image, enhancement)
        for x,y in image.copy():
            if abs(x) > BOUNDARY or abs(y) > BOUNDARY:
                image.discard((x,y))
        print(2+i*2, len(image))

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