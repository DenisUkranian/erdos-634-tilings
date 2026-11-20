#!/usr/bin/env python3
"""Independently check a positive F2 tile list using exact metric currents.

The generator's endpoint formulas and row indices are not imported.  A finite
nonnegative polygon family with exactly the board's oriented edge current has
covering multiplicity one inside and zero outside (see ENDPOINT_DUAL.md).
Consequently exact current cancellation certifies nonoverlap as well as cover.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import json


UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def scale(k, p):
    return k * p[0], k * p[1]


def mul(p, q):
    x, y = p
    u, v = q
    return x*u-y*v, x*v+y*u+y*v


def power(z, n):
    if n < 0:
        # z is a unit: its inverse is its complex conjugate.
        z, n = (z[0] + z[1], -z[1]), -n
    result = (F(1), F(0))
    while n:
        if n & 1:
            result = mul(result, z)
        z = mul(z, z)
        n >>= 1
    return result


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def norm(p):
    x, y = p
    return x*x+x*y+y*y


def axis(v):
    # A rational projective direction suffices; no square root or floating point.
    x, y = v
    if x:
        return F(1), y/x
    assert y, 'Zero-length edge'
    return F(0), F(1)


def current(poly):
    ans = Counter()
    for p, q in zip(poly, poly[1:]+poly[:1]):
        direction = axis(sub(q, p))
        ans[p, direction] += 1
        ans[q, direction] -= 1
    return ans


def check(data):
    if not __debug__:
        raise RuntimeError('Exact verification requires assertions; run without -O.')
    if data.get('format') != 'positive-endpoint-tiling-v1':
        raise ValueError('Unsupported positive certificate format')
    a, b, c = data['sides']
    assert all(type(x) is int for x in (a, b, c))
    assert a > b > 0 and c*c == a*a+a*b+b*b
    A, B = b*(2*a+b), a*(a+2*b)
    N = (a+2*b)*(2*a+b)
    assert data['N'] == N and len(data['tiles']) == N, 'Wrong tile count'
    board = ((F(0), F(0)), (F(A), F(0)), (F(0), F(B)))
    balance = Counter({r: -v for r, v in current(board).items()})
    seen = set()
    doubled_area = F(0)
    units = {}
    heights = Counter()
    denominators = []
    for i, item in enumerate(data['tiles']):
        q0, h, j, s = item
        assert len(q0) == 3 and all(type(v) is int for v in q0)
        assert all(type(v) is int for v in (h, j, s))
        x, y, e = q0
        assert e >= 0 and s in (-1, 1)
        q = (F(x, c**e), F(y, c**e))
        if h not in units:
            units[h] = power((F(a, c), F(b, c)), h)
        u = mul(units[h], UNITS[j % 6])
        v = mul(units[h], UNITS[(j+s) % 6])
        tri = (add(q, scale(-a, u)), q, add(q, scale(b, v)))
        area = det(sub(tri[1], tri[0]), sub(tri[2], tri[0]))
        assert abs(area) == a*b, ('Wrong area', i)
        if area < 0:
            tri = tri[::-1]
        assert sorted(norm(sub(tri[k], tri[(k+1) % 3])) for k in range(3)) == sorted((a*a, b*b, c*c)), ('Wrong metric', i)
        assert all(X >= 0 and Y >= 0 and B*X+A*Y <= A*B for X, Y in tri), ('Outside board', i)
        key = tuple(sorted(tri))
        assert key not in seen, ('Duplicated physical placement', i)
        seen.add(key)
        balance.update(current(tri))
        doubled_area += abs(area)
        heights[h] += 1
        denominators.extend(t.denominator for p in tri for t in p)
    assert doubled_area == A*B, 'Area mismatch'
    residual = [(r, v) for r, v in balance.items() if v]
    assert not residual, ('Uncancelled endpoint currents', len(residual), residual[:3])
    return dict(verified_positive_tiling=True, N=N, sides=[a, b, c],
                board_sides=sorted((A, B, c*c)),
                distinct_placements=len(seen), metric='x^2+xy+y^2',
                doubled_axial_area=str(doubled_area),
                short_height_counts=dict(sorted(heights.items())),
                largest_coordinate_denominator=max(denominators),
                endpoint_residual_count=0,
                verification='Exact metric, containment, area, and oriented endpoint-current cancellation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate')
    args = parser.parse_args()
    try:
        print(json.dumps(check(json.loads(Path(args.certificate).read_text())), indent=2))
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print(json.dumps(dict(verified_positive_tiling=False, error=str(error)), indent=2))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
