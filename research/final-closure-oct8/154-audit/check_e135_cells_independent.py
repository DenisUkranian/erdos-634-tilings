#!/usr/bin/env python3
"""Independent exact audit of the E45 98-tile-tail cell-containment bound.

No import of cell_bound.py. Uses forward physical coordinates, rational
polygon clipping, and direct containment of all three cell vertices.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def multiply(p, q):
    a, b = p
    c, d = q
    return a*c-b*d, a*d+b*c+b*d


def clip(polygon, inequality):
    a, b, c = inequality
    answer = []
    for start, end in zip(polygon, polygon[1:]+polygon[:1]):
        s = a*start[0]+b*start[1]-c
        t = a*end[0]+b*end[1]-c
        if s <= 0:
            answer.append(start)
        if (s < 0 < t) or (t < 0 < s):
            ratio = s/(s-t)
            answer.append((start[0]+ratio*(end[0]-start[0]),
                           start[1]+ratio*(end[1]-start[1])))
    return list(dict.fromkeys(answer))


def canonical(inequality):
    denominator = math.lcm(*(x.denominator for x in inequality))
    integers = [int(x*denominator) for x in inequality]
    divisor = math.gcd(*integers)
    integers = [x//divisor for x in integers]
    if next(x for x in integers if x) < 0:
        integers = [-x for x in integers]
    return tuple(integers)


def compute(k):
    scale = (Q(7), Q(0))
    for _ in range(k):
        scale = multiply(scale, (Q(3, 7), Q(5, 7)))
    a, b = scale
    require(a*a+a*b+b*b == 49, "physical scale has wrong norm")
    normals = [(-a, b, Q(0)), (-b, -a-b, Q(0)),
               (a+b, a, Q(45))]
    square = [(Q(0), Q(0)), (Q(1), Q(0)),
              (Q(1), Q(1)), (Q(0), Q(1))]
    shapes = [[(0, 0), (1, 0), (0, 1)],
              [(1, 0), (1, 1), (0, 1)]]
    cells = []
    lines = {(1, 0, 0), (1, 0, 1), (0, 1, 0), (0, 1, 1)}
    # In the normalized target |w|<=45/7. Each Eisenstein coordinate
    # has absolute value <=2|w|/sqrt(3)<8. A cell anchor differs from
    # a contained cell vertex by at most two in either coordinate.
    # [-12,12]^2 therefore strictly contains every possible anchor.
    for x in range(-12, 13):
        for y in range(-12, 13):
            for kind, offsets in enumerate(shapes):
                vertices = [(x+u, y+v) for u, v in offsets]
                constraints = [(nx, ny, limit-max(nx*u+ny*v for u, v in vertices))
                               for nx, ny, limit in normals]
                polygon = square[:]
                for constraint in constraints:
                    polygon = clip(polygon, constraint)
                    if not polygon:
                        break
                if polygon:
                    cells.append((kind, vertices))
                    lines.update(map(canonical, constraints))
    points = set()
    for (a, b, c), (d, e, f) in combinations(sorted(lines), 2):
        determinant = a*e-b*d
        if determinant:
            p = (Q(c*e-b*f, determinant), Q(a*f-c*d, determinant))
            if all(0 <= coordinate <= 1 for coordinate in p):
                points.add(p)
    maxima = [0, 0]
    balanced = 0
    for translation in points:
        counts = [0, 0]
        for kind, vertices in cells:
            contained = True
            for u, v in vertices:
                physical = multiply(scale, (u+translation[0], v+translation[1]))
                if not (physical[0] >= 0 and physical[1] >= 0
                        and physical[0]+physical[1] <= 45):
                    contained = False
                    break
            if contained:
                counts[kind] += 1
        maxima = [max(x, y) for x, y in zip(maxima, counts)]
        balanced = max(balanced, min(counts))
    return dict(k=k, potential_cells=len(cells), lines=len(lines),
                arrangement_vertices=len(points), individual_maxima=maxima,
                maximum_balanced_pairs=balanced, tail98_excluded=balanced < 15)


def main():
    here = Path(__file__).resolve().parent
    prior = json.loads((here.parent/'e135-structure/cell_bound_checked.json').read_text())
    records = []
    for reference in prior['records']:
        record = compute(reference['k'])
        require(all(reference[key] == value for key, value in record.items()),
                f"independent mismatch at k={reference['k']}")
        require(record['tail98_excluded'], "98-tail not excluded")
        records.append(record)
    require([record['k'] for record in records] == [1, 2, 3], "incomplete three-case coverage")
    sources = [Path(__file__), here.parent/'e135-structure/cell_bound.py',
               here.parent/'e135-structure/NO_GAPS.md']
    result = dict(status='PASS', independent_forward_coordinate_clipping=True,
                  direct_physical_vertex_containment=True, records=records,
                  hashes={str(path.relative_to(here.parent)):hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources})
    output = here/'e135_cells_independent.json'
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
