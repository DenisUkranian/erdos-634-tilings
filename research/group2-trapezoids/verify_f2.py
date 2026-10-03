#!/usr/bin/env python3
"""Independent exact unit-certificate checker, with all-pairs convex clipping.

Does not import the constructor or assume its grid/partition geometry.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def area2(poly):
    return sum(p[0]*poly[(i+1) % len(poly)][1]-p[1]*poly[(i+1) % len(poly)][0]
               for i, p in enumerate(poly))


def read_triangle(raw):
    need(isinstance(raw, list) and len(raw) == 3, 'Expected triangle')
    need(all(isinstance(p, list) and len(p) == 2 for p in raw), 'Bad coordinate dimensions')
    poly = [tuple(F(x) for x in p) for p in raw]
    need(area2(poly) != 0, 'Degenerate triangle')
    return poly if area2(poly) > 0 else poly[::-1]


def sides2(poly):
    ans = []
    for i, p in enumerate(poly):
        q = poly[(i+1) % 3]
        x, y = p[0]-q[0], p[1]-q[1]
        ans.append(x*x+x*y+y*y)
    return sorted(ans)


def clip(poly, triangle):
    result = list(poly)
    for i, p in enumerate(triangle):
        q = triangle[(i+1) % 3]
        old, result = result, []
        if not old:
            break
        last = old[-1]
        dl = det(p, q, last)
        for cur in old:
            dc = det(p, q, cur)
            if (dl >= 0) != (dc >= 0):
                t = dl/(dl-dc)
                result.append(tuple(x+t*(y-x) for x, y in zip(last, cur)))
            if dc >= 0:
                result.append(cur)
            last, dl = cur, dc
    return result


def verify(data):
    need(data.get('format') == 'ERDOS634_F2_UNIT_TRIANGLES_V1', 'Wrong format')
    a, b, c = data['tile']
    m, count = data['multiplier'], data['count']
    need(all(type(x) is int and x > 0 for x in (a, b, c, m, count)), 'Bad integers')
    need(a > b and c*c == a*a+a*b+b*b, 'Wrong reversed theorem domain')
    need(count == (a+2*b)*(2*a+b)*m*m, 'Wrong claimed count')
    need(data.get('coordinate_metric') == 'x^2+x*y+y^2', 'Wrong metric')
    target = read_triangle(data['target'])
    need(sides2(target) == sorted([(m*a*(a+2*b))**2, (m*b*(2*a+b))**2,
                                  (m*c*c)**2]), 'Wrong target sides')
    triangles = [read_triangle(raw) for raw in data['triangles']]
    need(len(triangles) == count, 'Wrong number of triangles')
    expected = sorted([a*a, b*b, c*c])
    total = F(0)
    for i, tri in enumerate(triangles):
        need(sides2(tri) == expected, f'Noncongruent tile {i}')
        need(all(det(target[j], target[(j+1) % 3], p) >= 0
                 for j in range(3) for p in tri), f'Tile {i} outside target')
        total += area2(tri)
    need(total == area2(target), 'Area does not cover target')
    boxes = [(min(x for x, y in tri), max(x for x, y in tri),
              min(y for x, y in tri), max(y for x, y in tri)) for tri in triangles]
    clipped = 0
    for i, tri in enumerate(triangles):
        l, r, d, u = boxes[i]
        for j in range(i):
            l2, r2, d2, u2 = boxes[j]
            # Exact bounds in an invertible affine coordinate system.
            if r <= l2 or r2 <= l or u <= d2 or u2 <= d:
                continue
            intersection = clip(tri, triangles[j])
            clipped += 1
            need(len(intersection) < 3 or area2(intersection) == 0,
                 f'Positive-area overlap {i},{j}')
    return {'status': 'PASS', 'tile': [a, b, c], 'multiplier': m,
            'unit_triangles': count, 'pairs_checked': count*(count-1)//2,
            'pairs_clipped_after_exact_bounds': clipped, 'arithmetic': 'exact rational',
            'coverage_basis': 'Containment, pairwise disjoint interiors, and equal total area',
            'full_Erdos634_solved': False, 'external_peer_review': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificate', type=Path)
    args = ap.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text())), indent=2))
