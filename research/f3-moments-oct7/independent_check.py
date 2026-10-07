#!/usr/bin/env python3
"""Check the frozen moment witness directly, without the LP model or scipy."""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def mul(p, q):
    return (p[0]*q[0] - p[1]*q[1],
            p[0]*q[1] + p[1]*q[0] + p[1]*q[1])


def power(p, n):
    if n < 0:
        p = (p[0] + p[1], -p[1])
        n = -n
    ans = (F(1), F(0))
    for _ in range(n):
        ans = mul(ans, p)
    return ans


def scale(n, p):
    return (n*p[0], n*p[1])


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def norm(p):
    return p[0]*p[0] + p[0]*p[1] + p[1]*p[1]


def area2(poly):
    return sum(det(p, q) for p, q in zip(poly, poly[1:] + poly[:1]))


def check(path):
    data = json.loads(path.read_text())
    a, b, c = data['parameters']
    assert (a, b, c) == (24, 11, 31)
    assert c*c == a*a + a*b + b*b
    z, rho = (F(a, c), F(b, c)), (F(0), F(1))
    target = [(F(0), F(0)), (F(c*c), F(0)),
              scale(c*(a+2*b), power(z, 3))]
    assert target == [tuple(map(F, p)) for p in data['target']]
    N = 3*(a+b)*(a+2*b)
    assert data['count'] == N == 4830
    assert area2(target) == N*a*b > 0

    hs = [t['height'] for t in data['types']]
    unit = {(h, j): mul(power(z, h), power(rho, j))
            for h in range(min(hs)-1, max(hs)+2) for j in range(3)}
    assert all(norm(v) == 1 for v in unit.values())

    def moments(poly, side_lengths):
        ans = defaultdict(lambda: [F(0), F(0), F(0)])
        for p, q in zip(poly, poly[1:] + poly[:1]):
            vector = sub(q, p)
            lengths = [L for L in side_lengths if norm(vector) == L*L]
            assert len(lengths) == 1
            L = lengths[0]
            matches = [(key, sign) for key, v in unit.items()
                       for sign in (-1, 1) if vector == scale(sign*L, v)]
            assert len(matches) == 1
            key, sign = matches[0]
            ans[key][0] += sign*L
            ans[key][1] += sign*L*(p[0]+q[0])/2
            ans[key][2] += sign*L*(p[1]+q[1])/2
        return ans

    total = defaultdict(lambda: [F(0), F(0), F(0)])
    centroid = [F(0), F(0)]
    population = defaultdict(int)
    inequalities = 0
    actual_count = 0
    placements = []
    for t in data['types']:
        n = t['multiplicity']
        assert isinstance(n, int) and n > 0
        h, j, ch = t['height'], t['rotation'], t['chirality']
        assert ch in (0, 1) and isinstance(h, int) and isinstance(j, int)
        rotation = mul(power(z, h), power(rho, j))
        reference = [(F(0), F(0)), (F(a), F(0)), (F(a), F(b))]
        if ch:
            reference = [(p[0]+p[1], -p[1]) for p in reference[::-1]]
        shift = tuple(map(F, t['translation']))
        triangle = [add(shift, mul(rotation, p)) for p in reference]
        assert area2(triangle) == a*b
        assert sorted(norm(sub(p, q)) for p, q in
                      zip(triangle, triangle[1:] + triangle[:1])) == sorted([a*a,b*b,c*c])
        for p, q in zip(target, target[1:] + target[:1]):
            for vertex in triangle:
                assert det(sub(q, p), sub(vertex, p)) >= 0
                inequalities += 1
        for key, values in moments(triangle, (a,b,c)).items():
            for k in range(3):
                total[key][k] += n*values[k]
        for k in range(2):
            centroid[k] += n*sum(p[k] for p in triangle)/3
        population[h] += n
        actual_count += n
        placements.append((n, triangle))

    assert actual_count == N
    boundary = moments(target, (c*c, c*(a+2*b), 3*b*(a+b)))
    for key in set(total) | set(boundary):
        assert total[key] == boundary[key]
    assert centroid == [N*sum(p[k] for p in target)/3 for k in range(2)]
    assert dict(population) == {1: 93, 2: 4737}
    assert all(n % c == 0 for h, n in population.items() if h != 2)
    assert population[2] % c == N % c
    # A repeated positive-area triangle gives an explicit interior overlap.
    n, tri = max(placements, key=lambda item: item[0])
    assert n > 1 and area2(tri) > 0
    return {'status': 'PASS', 'full_Erdos634_solved': False,
            'count': N, 'distinct_placements': len(placements),
            'height_populations': dict(population),
            'nonzero_direction_groups': len(set(total) | set(boundary)),
            'exact_containment_inequalities': inequalities,
            'largest_identical_stack': n,
            'tile_congruence': True, 'target_containment': True,
            'zeroth_and_first_directed_edge_moments': True,
            'area_and_area_centroid': True,
            'has_interior_overlap': True, 'is_tiling': False,
            'scope': 'The stated conditions do not certify this placement as a tiling and cannot exclude 4830. Existence of a genuine tiling is not decided.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=Path(__file__).with_name('exact-4830.json'))
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit('Run without -O: exact verification uses assertions.')
    report = check(args.source)
    out = json.dumps(report, sort_keys=True, indent=2) + '\n'
    if args.report:
        args.report.write_text(out)
    print(out, end='')


if __name__ == '__main__':
    main()
