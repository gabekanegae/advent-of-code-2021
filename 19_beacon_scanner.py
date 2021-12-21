##################################
# --- Day 19: Beacon Scanner --- #
##################################

from itertools import combinations
from collections import defaultdict, deque
import AOCUtils

# http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
rotations = [
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

def rotate_vectors(rotation, p):
    return tuple(sum(a * b for a, b in zip(p, row)) for row in rotation)

def add_vectors(a, b):
    return tuple(pa + pb for pa, pb in zip(a, b))

def sub_vectors(a, b):
    return tuple(pa - pb for pa, pb in zip(a, b))

def distance_vectors(a, b):
    return tuple(abs(pa - pb) for pa, pb in zip(a, b))

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
        
        # Apply any existing rotation and translation to all beacons
        if self.rot is not None:
            self._absolute_beacons = set(rotate_vectors(self.rot, p) for p in self._absolute_beacons)
        if self.pos is not None:
            self._absolute_beacons = set(add_vectors(self.pos, p) for p in self._absolute_beacons)
        
        return self._absolute_beacons

    @property
    def distances(self):
        # Compute all n*(n-1)/2 distances between beacons,
        # together with the beacon coordinates for lookup
        return {tuple(sorted(distance_vectors(a, b))): (a, b) for a, b in combinations(self.beacons, 2)}

def find_transformation(cur, ref):
    # From the list of common distances, pick any arbitrary line segment
    common_distances = cur.distances.keys() & ref.distances.keys()
    distance = common_distances.pop()

    # Get the two pairs of points related to that line segment, one from the
    # reference beacon and another from the current, to-be-matched, beacon
    cur_pair = cur.distances[distance]
    ref_pair = ref.distances[distance]

    # For each of the 24 rotations, rotate the pair from the current beacon
    # and solve for a translation that would take the current line segment
    # to the reference line segment
    for rot in rotations:
        rotated_cur_pair = tuple(rotate_vectors(rot, p) for p in cur_pair)

        # Attempt the two possible translations after this rotation,
        # if none of them are valid, keep trying the other rotations
        
        # {cur[0]: ref[0], cur[1]: ref[1]}
        translation = [sub_vectors(b, a) for a, b in zip(rotated_cur_pair, ref_pair)]
        if translation[0] == translation[1]:
            pos = translation[0]
            return pos, rot

        # {cur[0]: ref[1], cur[1]: ref[0]}
        translation = [sub_vectors(b, a) for a, b in zip(rotated_cur_pair, reversed(ref_pair))]
        if translation[0] == translation[1]:
            pos = translation[0]
            return pos, rot

    return None, None

def reconstruct_map(scanners):
    # Create graph of connected scanners
    connections = defaultdict(set)
    for a, b in combinations(scanners, 2):
        # Scanners are connected if they have at least 12 beacons in common,
        # i.e. C(12,2) = 66 beacon-to-beacon distances
        if len(a.distances.keys() & b.distances.keys()) >= 66:
            connections[a.scanner_id].add(b.scanner_id)
            connections[b.scanner_id].add(a.scanner_id)

    # Set scanner #0 as global origin
    scanners[0].rot = rotations[0]
    scanners[0].pos = (0, 0, 0)

    # BFS through all scanners, rotating and translating their
    # coordinates to match scanner #0 as global origin
    queue = deque([(0, None)])
    known_scanners = set()
    while queue: 
        cur_id, ref_id = queue.popleft()

        if cur_id in known_scanners: continue
        known_scanners.add(cur_id)

        for connection_id in connections[cur_id]:
            # Store parent scanner as reference
            queue.append((connection_id, cur_id))

        # Ignore transformations for scanner #0 as it is set as global origin
        if cur_id == 0: continue

        # Compute and apply transformation to current scanner   
        cur = scanners[cur_id]
        ref = scanners[ref_id]
        cur.pos, cur.rot = find_transformation(cur, ref)

##################################

raw_scanners = AOCUtils.load_input(19)

raw_scanners = '\n'.join(raw_scanners).split('\n\n')

scanners = []
for scanner_id, raw_scanner in enumerate(raw_scanners):
    raw_scanner = raw_scanner.splitlines()[1:]

    scanner = Scanner(scanner_id, raw_scanner)
    scanners.append(scanner)

reconstruct_map(scanners)

unique_beacons = set().union(*(scanner.beacons for scanner in scanners))
print(f'Part 1: {len(unique_beacons)}')

max_distance = max(sum(distance_vectors(a.pos, b.pos)) for a, b in combinations(scanners, 2))
print(f'Part 2: {max_distance}')

AOCUtils.print_time_taken()