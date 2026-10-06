#!/usr/bin/env python3
"""Independent exact checker for explicit F2/F3/F4 unit-triangle certificates.

Does not import the construction.  Positive-area overlap is tested by the
separating-axis theorem, independently of the older clipping checker.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def triangle(raw):
    require(isinstance(raw, list) and len(raw) == 3, 'Expected three vertices')
    require(all(isinstance(p, list) and len(p) == 2 for p in raw), 'Bad coordinates')
    require(all(type(x) is int or isinstance(x, str) for p in raw for x in p),
            'Coordinates must be exact integers or rational strings')
    points = [tuple(Fraction(x) for x in p) for p in raw]
    area = det(*points)
    require(area != 0, 'Degenerate triangle')
    return points if area > 0 else [points[0], points[2], points[1]]


def squared_lengths(points):
    values = []
    for p, q in zip(points, points[1:]+points[:1]):
        x, y = p[0]-q[0], p[1]-q[1]
        values.append(x*x+x*y+y*y)
    return sorted(values)


def separated(left, right):
    # Every polygon is CCW.  A separating axis of two convex polygons can be
    # chosen normal to one of their edges.  Equality permits boundary contact.
    for polygon, other in ((left, right), (right, left)):
        for p, q in zip(polygon, polygon[1:]+polygon[:1]):
            if all(det(p, q, r) <= 0 for r in other):
                return True
    return False


def verify(data):
    require(data.get('coordinate_metric') == 'x^2+x*y+y^2', 'Unsupported metric')
    a, b, c = data['tile']
    m, count = data['multiplier'], data['count']
    require(all(type(x) is int and x > 0 for x in (a, b, c, m, count)),
            'Expected positive integer parameters')
    require(c*c == a*a+a*b+b*b, 'Tile does not have a 120-degree angle')
    candidates = {
        'F2': ((a+2*b)*(2*a+b), (c*c, a*(a+2*b), b*(2*a+b))),
        'F3': (3*(a+2*b)*(a+b), (c*c, c*(a+2*b), 3*b*(a+b))),
        'F4': ((2*a+b)*(a+b), (a*c, b*(2*a+b), c*(a+b))),
    }
    family = next((f for f in candidates
                   if data.get('format') == f'ERDOS634_{f}_UNIT_TRIANGLES_V1'), None)
    require(family is not None, 'Unsupported certificate format')
    coefficient, target_sides = candidates[family]
    require(count == coefficient*m*m, 'Wrong family tile count')
    target = triangle(data['target'])
    require(squared_lengths(target) == sorted((m*s)**2 for s in target_sides),
            'Wrong target side lengths')
    tiles = [triangle(t) for t in data['triangles']]
    require(len(tiles) == count, 'Wrong actual tile count')
    expected = sorted((a*a, b*b, c*c))
    area = 0
    for i, tile in enumerate(tiles):
        require(squared_lengths(tile) == expected, f'Noncongruent tile {i}')
        require(all(det(p, q, r) >= 0 for p, q in zip(target, target[1:]+target[:1])
                    for r in tile), f'Tile {i} is not contained in the target')
        area += det(*tile)
    require(area == det(*target), 'Total tile area differs from target area')
    bounds = [(min(p[0] for p in t), max(p[0] for p in t),
               min(p[1] for p in t), max(p[1] for p in t)) for t in tiles]
    axis_tests = 0
    for i, tile in enumerate(tiles):
        x0, x1, y0, y1 = bounds[i]
        for j in range(i):
            u0, u1, v0, v1 = bounds[j]
            if x1 <= u0 or u1 <= x0 or y1 <= v0 or v1 <= y0:
                continue
            axis_tests += 1
            require(separated(tile, tiles[j]), f'Positive-area overlap {i}, {j}')
    return {'status': 'PASS', 'family': family, 'tile': [a, b, c],
            'multiplier': m, 'N': count,
            'target_side_lengths': sorted(m*s for s in target_sides),
            'pairs_checked': count*(count-1)//2,
            'separating_axis_checks_after_exact_bounds': axis_tests,
            'arithmetic': 'exact rational',
            'coverage_basis': 'Containment, pairwise disjoint interiors, equal total area',
            'full_Erdos634_solved': False, 'external_peer_review': False}


def main():
    if not __debug__:
        raise SystemExit('Run without -O so all verification gates remain enabled')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    report = verify(json.loads(raw))
    report['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
