#!/usr/bin/env python3
"""Exact four-region F4 construction for 0<a<b, c^2=a^2+ab+b^2.

Coordinates (x,y) represent x+y*exp(i*pi/3). Reflections are permitted.
This module generates positive unit triangles; it does not decide other rays.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def add(p, q):
    return tuple(x+y for x, y in zip(p, q))


def sub(p, q):
    return tuple(x-y for x, y in zip(p, q))


def mul(k, p):
    return tuple(k*x for x in p)


def grid(p, q, r, n, omit_corner=0):
    """Retain the n-grid after deleting the integer corner at p."""
    u, v = mul(F(1, n), sub(q, p)), mul(F(1, n), sub(r, p))
    for i in range(n):
        for j in range(n-i):
            o = add(p, add(mul(i, u), mul(j, v)))
            x, y = add(o, u), add(o, v)
            if i+j >= omit_corner:
                yield [o, x, y]
            if i+j < n-1 and i+j >= omit_corner-1:
                yield [x, add(x, v), y]


def construct(a, b, c, m=1):
    if not all(type(x) is int for x in (a, b, c, m)):
        raise ValueError('Parameters must be integers')
    if not (0 < a < b and c*c == a*a+a*b+b*b and m > 0):
        raise ValueError('Require 0<a<b, c^2=a^2+ab+b^2, and m>=1')
    u = (F(b), F(a))
    o = (F(0), F(0))
    A, B = (F(b*c), F(0)), mul(c, u)
    D, C = (F((a+b)*c), F(0)), mul(F(b*(2*a+b), c), u)
    E, H = add(A, mul(F(a*b, c), u)), add(A, (F(0), F(b*c)))
    target = [mul(m, p) for p in (o, D, C)]
    regions = [(o, A, B, c, 0), (A, D, E, a, 0),
               (D, C, E, a, 0), (H, A, E, b, b-a)]
    triangles = []
    for p, q, r, n, omitted in regions:
        triangles.extend(grid(mul(m, p), mul(m, q), mul(m, r), m*n, m*omitted))

    def encode(poly):
        return [[str(x), str(y)] for x, y in poly]

    return {'format': 'ERDOS634_F4_UNIT_TRIANGLES_V1',
            'coordinate_metric': 'x^2+x*y+y^2', 'tile': [a, b, c],
            'multiplier': m, 'count': (2*a+b)*(a+b)*m*m,
            'target': encode(target), 'triangles': list(map(encode, triangles))}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('a', type=int)
    ap.add_argument('b', type=int)
    ap.add_argument('c', type=int)
    ap.add_argument('--multiplier', type=int, default=1)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    data = construct(args.a, args.b, args.c, args.multiplier)
    args.output.write_text(json.dumps(data, indent=2)+'\n')
    print(f"Wrote {data['count']} explicit congruent triangles to {args.output}")
