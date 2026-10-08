#!/usr/bin/env python3
"""Exact local 14-tile placement and surviving 21-tile inventory; no E135 tiling."""
from collections import defaultdict
from math import gcd
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/final-closure-oct8/e60-inventory'))
import line_filter as lines


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def norm(p):
    x, y = p
    return x*x+x*y+y*y


def edges(t):
    return list(zip(t, t[1:]+t[:1]))


def separates(t, u):
    return any(all(det(sub(b, a), sub(p, a)) <= 0 for p in u)
               for a, b in edges(t))


def main():
    if not __debug__:
        raise RuntimeError('Run without -O so exact assertions execute.')
    triangles = []
    for k in range(7):
        p = (9*k, 15*k)
        q = (9*k+49, 15*k)
        r = (9*(k+1), 15*(k+1))
        s = (9*(k+1)+49, 15*(k+1))
        triangles.extend([[p, q, r], [q, s, r]])
    short_current = defaultdict(int)
    for t in triangles:
        assert sum(det(a, b) for a, b in edges(t)) == 735
        assert sorted(norm(sub(b, a)) for a, b in edges(t)) == [441, 1225, 2401]
        assert all(x >= 0 and y >= 0 and x+y <= 315 for x, y in t)
        for a, b in edges(t):
            v = sub(b, a)
            n2 = norm(v)
            if n2 == 2401:
                assert v[1] == 0  # All long edges have height zero.
                continue
            length = 3 if n2 == 441 else 5
            g = gcd(abs(v[0]), abs(v[1]))
            d = (v[0]//g, v[1]//g)
            sign = 1
            if d[0] < 0 or (d[0] == 0 and d[1] < 0):
                d = (-d[0], -d[1])
                sign = -1
            assert d in ((3, 5), (8, -3))  # z and rho^-1 z directions.
            short_current[d, det(d, a)] += sign*length
    for i, t in enumerate(triangles):
        for u in triangles[:i]:
            assert separates(t, u) or separates(u, t)
    assert all(v % 7 == 0 for v in short_current.values())
    assert sorted(v for v in short_current.values() if v) == [-21, 21]

    inv = [0]*12
    inv[0] = inv[3] = inv[11] = 7
    totals = [[0]*4 for _ in range(3)]
    for n, ee in zip(inv, lines.EDGES):
        for j, kind in ee:
            totals[j][kind] += n
    assert all((3*(x[0]-x[1])+5*(x[2]-x[3])) % 7 == 0 for x in totals)
    records = []
    for index, (n, ee) in enumerate(zip(inv, lines.EDGES)):
        if not n:
            continue
        bounds = [lines.max_lines(tuple(totals[j]), kind, 38) for j, kind in ee]
        assert n <= bounds[0]*bounds[1]
        records.append({'orientation': ('A' if index < 6 else 'B')+str(index % 6),
                        'count': n, 'line_bounds': bounds,
                        'gamma_intersection_bound': bounds[0]*bounds[1]})

    certificate = {'format': 'exact_polygon_unit_v1', 'denominator': 7,
                   'tile': [3, 5, 7],
                   'target': [[0, 0], [49, 0], [112, 105], [63, 105]],
                   'triangles': triangles,
                   'scope': '14-tile local patch contained in E45; complement is not tiled'}
    report = {'status': 'PASS', 'E135_solved': False,
              'local_patch_tiles': 14, 'pair_checks': 91,
              'short_height': 1, 'long_height': 0,
              'short_line_nonzero_currents': [-21, 21],
              'contained_in_equilateral_side45': True,
              'formal_population21_inventory': inv,
              'formal_population21_line_totals': totals,
              'formal_population21_pigeonhole_tests': records}
    here = Path(__file__).resolve().parent
    (here/'local_fourteen.json').write_text(json.dumps(certificate, indent=2)+'\n')
    (here/'local_barriers_verified.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
