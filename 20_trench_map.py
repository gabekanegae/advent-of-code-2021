##############################
# --- Day 20: Trench Map --- #
##############################

import AOCUtils

mov9 = [
    (-1, -1), (-1, 0), (-1, 1),
     (0, -1),  (0, 0),  (0, 1),
     (1, -1),  (1, 0),  (1, 1)
    ]

class Image:
    def __init__(self, raw_image):
        # Store lit pixels when not flipped, and unlit pixels when flipped
        self.pixels = set()
        for x in range(len(raw_image)):
            for y in range(len(raw_image[0])):
                if raw_image[x][y] == '#':
                    self.pixels.add((x, y))

        self.flipped = False

    @property
    def bounding_box(self):
        px = [i[0] for i in self.pixels]
        py = [i[1] for i in self.pixels]
        return min(px), max(px), min(py), max(py)

    @property
    def lit_pixels_count(self):
        # If image is flipped, it has infinite lit pixels
        return len(self.pixels) if not self.flipped else float('inf')

    def _invert(self):
        min_x, max_x, min_y, max_y = self.bounding_box

        flipped_pixels = set()    
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                if (x, y) not in self.pixels:
                    flipped_pixels.add((x, y))

        self.pixels = flipped_pixels
        self.flipped = not self.flipped

    def enhance(self, enhancement):
        min_x, max_x, min_y, max_y = self.bounding_box

        new_pixels = set()
        for x in range(min_x-1, max_x+1+1):
            for y in range(min_y-1, max_y+1+1):
                bits = []
                for dx, dy in mov9:
                    # If flipped, flip bits
                    bit = ((x+dx, y+dy) in self.pixels) ^ self.flipped
                    bits.append(int(bit))

                idx = int(''.join(map(str, bits)), 2)
                if enhancement[idx] == '#':
                    new_pixels.add((x,y))

        self.pixels = new_pixels

        # This check is not needed for the actual input (it's true for every
        # real input), but this makes it work for any enhancement that may
        # not have the flip behavior (like the example given)
        has_flip_behavior = (enhancement[2**0 - 1] == '#' and enhancement[2**9 - 1] == '.')
        if has_flip_behavior:
            if self.flipped:
                self.flipped = False
            else:
                self._invert()

##############################

raw_data = AOCUtils.load_input(20)

enhancement = raw_data[0]
raw_image = raw_data[2:]

image = Image(raw_image)
for _ in range(2):
    image.enhance(enhancement)

print(f'Part 1: {image.lit_pixels_count}')

image = Image(raw_image)
for _ in range(50):
    image.enhance(enhancement)

print(f'Part 2: {image.lit_pixels_count}')

AOCUtils.print_time_taken()