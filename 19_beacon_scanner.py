##################################
# --- Day 19: Beacon Scanner --- #
##################################

from itertools import combinations
from collections import defaultdict, deque
import AOCUtils

# http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
rotation_matrices = [
    (( 1, 0, 0), ( 0, 1, 0), ( 0, 0, 1)), # ( x,  y,  z)
    (( 1, 0, 0), ( 0, 0,-1), ( 0, 1, 0)), # ( x, -z,  y)
    (( 1, 0, 0), ( 0,-1, 0), ( 0, 0,-1)), # ( x, -y, -z)
    (( 1, 0, 0), ( 0, 0, 1), ( 0,-1, 0)), # ( x,  z, -y)
    (( 0,-1, 0), ( 1, 0, 0), ( 0, 0, 1)), # (-y,  x,  z)
    (( 0, 0, 1), ( 1, 0, 0), ( 0, 1, 0)), # ( z,  x,  y)
    (( 0, 1, 0), ( 1, 0, 0), ( 0, 0,-1)), # ( y,  x, -z)
    (( 0, 0,-1), ( 1, 0, 0), ( 0,-1, 0)), # (-z,  x, -y)
    ((-1, 0, 0), ( 0,-1, 0), ( 0, 0, 1)), # (-x, -y,  z)
    ((-1, 0, 0), ( 0, 0,-1), ( 0,-1, 0)), # (-x, -z, -y)
    ((-1, 0, 0), ( 0, 1, 0), ( 0, 0,-1)), # (-x,  y, -z)
    ((-1, 0, 0), ( 0, 0, 1), ( 0, 1, 0)), # (-x,  z,  y)
    (( 0, 1, 0), (-1, 0, 0), ( 0, 0, 1)), # ( y, -x,  z)
    (( 0, 0, 1), (-1, 0, 0), ( 0,-1, 0)), # ( z, -x, -y)
    (( 0,-1, 0), (-1, 0, 0), ( 0, 0,-1)), # (-y, -x, -z)
    (( 0, 0,-1), (-1, 0, 0), ( 0, 1, 0)), # (-z, -x,  y)
    (( 0, 0,-1), ( 0, 1, 0), ( 1, 0, 0)), # (-z,  y,  x)
    (( 0, 1, 0), ( 0, 0, 1), ( 1, 0, 0)), # ( y,  z,  x)
    (( 0, 0, 1), ( 0,-1, 0), ( 1, 0, 0)), # ( z, -y,  x)
    (( 0,-1, 0), ( 0, 0,-1), ( 1, 0, 0)), # (-y, -z,  x)
    (( 0, 0,-1), ( 0,-1, 0), (-1, 0, 0)), # (-z, -y, -x)
    (( 0,-1, 0), ( 0, 0, 1), (-1, 0, 0)), # (-y,  z, -x)
    (( 0, 0, 1), ( 0, 1, 0), (-1, 0, 0)), # ( z,  y, -x)
    (( 0, 1, 0), ( 0, 0,-1), (-1, 0, 0)), # ( y, -z, -x)
]

def apply_rotation(rot_matrix, pos):
    return tuple(sum(a * b for a, b in zip(pos, row)) for row in rot_matrix)

def sum_vectors(a, b):
    return tuple(pa + pb for pa, pb in zip(a, b))

def sub_vectors(a, b):
    return tuple(pa - pb for pa, pb in zip(a, b))

def abs_vectors(a, b):
    return tuple(abs(pa - pb) for pa, pb in zip(a, b))

def multiply_matrices(a, b):
    return tuple(tuple(sum(pa * pb for pa, pb in zip(r_a, c_b)) for c_b in b) for r_a in a)

class Scanner:
    def __init__(self, scanner_id, raw_beacons):
        self.scanner_id = scanner_id

        self._relative_beacons = set()
        for raw_beacon in raw_beacons:
            beacon = tuple(map(int, raw_beacon.split(',')))
            self._relative_beacons.add(beacon)

        self.pos = None
        self.rot = None

    @property
    def beacons(self):
        self._absolute_beacons = self._relative_beacons

        if self.rot is None and self.pos is None:
            return self._absolute_beacons
        
        if self.rot is not None:
            self._absolute_beacons = set(apply_rotation(self.rot, p) for p in self._absolute_beacons)
        if self.pos is not None:
            self._absolute_beacons = set(sum_vectors(self.pos, p) for p in self._absolute_beacons)
        
        return self._absolute_beacons

    @property
    def distances(self):
        return {tuple(sorted(abs_vectors(a, b))): (a, b) for a, b in combinations(self.beacons, 2)}

def find_transformation(cur, ref):
    common_distances = cur.distances.keys() & ref.distances.keys()
    for distance in common_distances:
        cur_pair = cur.distances[distance]
        ref_pair = ref.distances[distance]

        for rot in rotation_matrices:
            rotated_cur_pair = tuple(apply_rotation(rot, p) for p in cur_pair)

            translation_1 = [sub_vectors(b, a) for a, b in zip(rotated_cur_pair, ref_pair)]
            translation_2 = [sub_vectors(b, a) for a, b in zip(reversed(rotated_cur_pair), ref_pair)]

            if translation_1[0] == translation_1[1]:
                pos = translation_1[0]
                return pos, rot
            elif translation_2[0] == translation_2[1]:
                pos = translation_2[0]
                return pos, rot

    return None, None

##################################

raw_scanners = AOCUtils.load_input(19)

raw_scanners = '\n'.join(raw_scanners).split('\n\n')

scanners = []
for scanner_id, raw_scanner in enumerate(raw_scanners):
    raw_scanner = raw_scanner.splitlines()[1:]

    scanner = Scanner(scanner_id, raw_scanner)
    scanners.append(scanner)

connections = defaultdict(set)
for a, b in combinations(scanners, 2):
    if len(a.distances.keys() & b.distances.keys()) >= 66: # C(12,2) = 12!/(2!*10!) = 66
        connections[a.scanner_id].add(b.scanner_id)
        connections[b.scanner_id].add(a.scanner_id)

scanners[0].rot = rotation_matrices[0]
scanners[0].pos = (0, 0, 0)

queue = deque([(0, None)])
known_scanners = set()
while queue:
    cur_id, ref_id = queue.popleft()

    if cur_id in known_scanners: continue
    known_scanners.add(cur_id)

    for connection_id in connections[cur_id]:
        queue.append((connection_id, cur_id))

    if cur_id == 0: continue

    cur = scanners[cur_id]
    ref = scanners[ref_id]

    cur.pos, cur.rot = find_transformation(cur, ref)

    intersec = cur.beacons & ref.beacons

beacons = set()
for scanner in scanners:
    beacons |= scanner.beacons

print(f'Part 1: {len(beacons)}')

max_distance = max(sum(abs_vectors(a.pos, b.pos)) for a, b in combinations(scanners, 2))
print(f'Part 2: {max_distance}')

AOCUtils.print_time_taken()