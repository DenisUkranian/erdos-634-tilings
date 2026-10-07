#!/usr/bin/env python3
"""Exact positive F3 tilings from a staircase of common ab-by-ab cells.

This construction uses one short-direction class in the gamma remainder.
The directory name records the research route, not a mixed-class claim.
"""
import argparse
from fractions import Fraction as F
import gzip
import json
from pathlib import Path


def add(p, q): return p[0]+q[0], p[1]+q[1]
def sub(p, q): return p[0]-q[0], p[1]-q[1]
def scale(k, p): return k*p[0], k*p[1]
def mul(p, q):
    return (p[0]*q[0]-p[1]*q[1],
            p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def encode(poly): return [[str(x), str(y)] for x, y in poly]


def grid(p, q, r, n):
    u, v = scale(F(1, n), sub(q, p)), scale(F(1, n), sub(r, p))
    for i in range(n):
        for j in range(n-i):
            o = add(p, add(scale(i, u), scale(j, v)))
            x, y = add(o, u), add(o, v)
            yield [o, x, y]
            if i+j < n-1:
                yield [x, add(x, v), y]


def staircase_cells(a, b, t):
    return [(i, j) for i in range((t-1)//a+1)
            for j in range((t-1-a*i)//b+1)]


def gamma_remainder(T, X, K, a, b, L, t):
    u, v = scale(F(1, L), sub(X, T)), scale(F(1, L), sub(K, T))
    cells = set(staircase_cells(a, b, t))
    for i in range(L):
        for j in range(L-i):
            if (i//b, j//a) in cells:
                continue
            o = add(T, add(scale(i, u), scale(j, v)))
            x, y = add(o, u), add(o, v)
            yield [o, x, y]
            if i+j < L-1:
                yield [x, add(x, v), y]
    u2, v2 = scale(F(b, a), u), scale(F(a, b), v)
    for i, j in sorted(cells):
        for s in range(a):
            for r in range(b):
                p, q = a*i+s, b*j+r
                o = add(T, add(scale(p, u2), scale(q, v2)))
                x, y = add(o, u2), add(o, v2)
                if p+q >= t:
                    yield [o, x, y]
                if p+q >= t-1:
                    yield [x, add(x, v2), y]


def construct(a, b, c, m=1):
    if any(type(x) is not int for x in (a, b, c, m)):
        raise ValueError('integer parameters required')
    if not (a > b > 0 and m > 0 and c*c == a*a+a*b+b*b):
        raise ValueError('require a>b>0, plus norm, and m>0')
    S, h, delta = c*c, a+2*b, a-b
    L, t = m*h, m*delta
    cost = b+a*((t+b-1)//b)
    if L < cost:
        raise ValueError(f'staircase does not fit: required {cost}, available {L}')
    # The fitting staircase contains the whole reflected corner, and thus
    # also guarantees the positivity of the established F3 macro partition.
    if h*b <= delta*a:
        raise ValueError('gamma macro is not positive')
    Z = F(a), F(b)
    Z2 = mul(Z, Z)
    X, Y = (F(0), F(0)), (F(m*S), F(0))
    I, J = scale(m*a, Z), scale(m, Z2)
    T = scale(F(m*a*h, S), Z2)
    K = scale(F(m*h, S), mul(Z2, Z))
    J2 = scale(m*a, mul((F(1), F(1)), Z))
    tiles = []
    for p, q, r in ((X, Y, I), (Y, I, J2), (X, I, J)):
        tiles.extend(grid(p, q, r, m*c))
    remainder = list(gamma_remainder(T, X, K, a, b, L, t))
    if len(remainder) != L*L-t*t:
        raise RuntimeError('gamma count mismatch')
    tiles.extend(remainder)
    count = 3*(a+b)*h*m*m
    if len(tiles) != count:
        raise RuntimeError('F3 count mismatch')
    return {
        'format': 'ERDOS634_F3_UNIT_TRIANGLES_V1',
        'coordinate_metric': 'x^2+x*y+y^2',
        'tile': [a, b, c], 'multiplier': m, 'count': count,
        'target': encode([X, Y, K]),
        'triangles': [encode(tri) for tri in tiles],
        'construction': 'three cR grids and a staircase of common ab-by-ab cells',
        'gamma_corner': {
            'outer_scale': L, 'removed_scale': t,
            'staircase_cells': [list(cell) for cell in staircase_cells(a, b, t)],
            'staircase_cost': cost, 'count': len(remainder)},
        'macro_vertices': {name: encode([p])[0] for name, p in
            [('X', X), ('Y', Y), ('I', I), ('J', J),
             ('J2', J2), ('T', T), ('K', K)]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('a', 'b', 'c'):
        parser.add_argument(key, type=int)
    parser.add_argument('--multiplier', type=int, default=1)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = construct(args.a, args.b, args.c, args.multiplier)
    raw = (json.dumps(data, separators=(',', ':'))+'\n').encode()
    args.output.write_bytes(gzip.compress(raw, mtime=0)
                            if args.output.suffix == '.gz' else raw)
    print(json.dumps({k: data[k] for k in
                      ('tile', 'multiplier', 'count', 'gamma_corner')}))


if __name__ == '__main__':
    main()
