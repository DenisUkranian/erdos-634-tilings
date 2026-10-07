#!/usr/bin/env python3
"""Independent exact unit-coordinate verifier with a complete spatial filter.

No constructor is imported. Rational box buckets avoid an unnecessary
quadratic loop while retaining a proof that every overlapping pair is tested.
"""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def decode(raw):
    require(isinstance(raw, list) and len(raw) == 3, 'three vertices required')
    require(all(isinstance(p, list) and len(p) == 2 for p in raw),
            'two coordinates required')
    require(all(type(x) is int or isinstance(x, str) for p in raw for x in p),
            'exact integer or rational-string coordinates required')
    p = [tuple(F(x) for x in v) for v in raw]
    area = det(*p)
    require(area != 0, 'degenerate triangle')
    return p if area > 0 else [p[0], p[2], p[1]]


def lengths(p):
    result = []
    for u, v in zip(p, p[1:]+p[:1]):
        x, y = u[0]-v[0], u[1]-v[1]
        result.append(x*x+x*y+y*y)
    return sorted(result)


def separated(left, right):
    for polygon, other in ((left, right), (right, left)):
        for p, q in zip(polygon, polygon[1:]+polygon[:1]):
            if all(det(p, q, r) <= 0 for r in other):
                return True
    return False


def verify(data):
    require(data.get('format') == 'ERDOS634_F3_UNIT_TRIANGLES_V1', 'bad format')
    require(data.get('coordinate_metric') == 'x^2+x*y+y^2', 'bad metric')
    a, b, c = data['tile']
    m, n = data['multiplier'], data['count']
    require(all(type(x) is int and x > 0 for x in (a, b, c, m, n)),
            'positive integer parameters required')
    require(c*c == a*a+a*b+b*b, 'plus norm fails')
    require(n == 3*(a+b)*(a+2*b)*m*m, 'wrong F3 count')
    target = decode(data['target'])
    sides = sorted(m*s for s in (c*c, c*(a+2*b), 3*b*(a+b)))
    require(lengths(target) == [x*x for x in sides], 'wrong F3 target')
    tiles = [decode(t) for t in data['triangles']]
    require(len(tiles) == n, 'wrong number of triangles')
    unit_lengths = sorted((a*a, b*b, c*c))
    total_area = F(0)
    bounds, buckets = [], {}
    box_candidates = sat_checks = 0
    for i, tile in enumerate(tiles):
        require(lengths(tile) == unit_lengths, f'noncongruent tile {i}')
        require(all(det(p, q, r) >= 0
                    for p, q in zip(target, target[1:]+target[:1]) for r in tile),
                f'tile {i} outside target')
        total_area += det(*tile)
        x0, x1 = min(v[0] for v in tile), max(v[0] for v in tile)
        y0, y1 = min(v[1] for v in tile), max(v[1] for v in tile)
        bounds.append((x0, x1, y0, y1))
        # Every closed rational bounding box is inserted into all unit cells
        # of this c-spaced grid that it meets, including both boundary cells.
        # Intersecting boxes share a bucket, so no positive overlap is missed.
        keys = [(x, y) for x in range(x0//c, x1//c+1)
                for y in range(y0//c, y1//c+1)]
        candidates = set()
        for key in keys:
            candidates.update(buckets.get(key, ()))
        box_candidates += len(candidates)
        for j in candidates:
            u0, u1, v0, v1 = bounds[j]
            if x1 <= u0 or u1 <= x0 or y1 <= v0 or v1 <= y0:
                continue
            sat_checks += 1
            require(separated(tile, tiles[j]), f'positive-area overlap {i}, {j}')
        for key in keys:
            buckets.setdefault(key, []).append(i)
    require(total_area == det(*target), 'area does not cover target')
    return {
        'status': 'PASS', 'family': 'F3', 'tile': [a, b, c],
        'multiplier': m, 'N': n, 'target_side_lengths': sides,
        'all_pair_count': n*(n-1)//2,
        'spatial_bucket_pair_candidates': box_candidates,
        'separating_axis_checks_after_exact_bounds': sat_checks,
        'arithmetic': 'exact rational',
        'coverage_basis': 'All triangles contained; a complete rational spatial '
                          'filter and separating axes exclude every positive '
                          'overlap; total area equals target area.',
        'full_Erdos634_solved': False, 'external_peer_review': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    decoded = gzip.decompress(raw) if args.certificate.suffix == '.gz' else raw
    report = verify(json.loads(decoded))
    report['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
