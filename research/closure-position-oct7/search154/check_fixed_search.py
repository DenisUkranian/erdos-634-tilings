#!/usr/bin/env python3
"""Independent Fraction checks of fixed-coordinate candidate generation.

This verifies the finite template/geometry implementation, not completion
of the search or exhaustion of its roots.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, isqrt
from pathlib import Path
import argparse
import json
import random
import subprocess

D = 13**11


def norm(p):
    x, y = p
    return x*x+x*y+y*y


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def direction(v):
    x, y = map(Q, v)
    x, y = x.numerator*y.denominator, y.numerator*x.denominator
    g = gcd(x, y)
    return x//g, y//g


def product(u, v):
    return u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0]+u[1]*v[1]


DIRS = {}
for sign in (-1, 1):
    p = (1, 0)
    for mag in range(13):
        q = p
        for r in range(6):
            DIRS[direction(q)] = (sign*mag, r)
            q = (-q[1], q[0]+q[1])
        p = product(p, (8, 7) if sign == 1 else (15, -7))


SEM = {7*a+8*b+13*c for a in range(23) for b in range(20)
       for c in range(12) if 7*a+8*b+13*c <= 154}


def valid(p):
    x, y = p
    if not (y >= 0 and 8*x >= 7*y and 8*x+15*y <= 1232):
        return False
    values = []
    if y == 0:
        values.append((154, x))
    if 8*x+15*y == 1232 or 8*x-7*y == 0:
        values.append((91, 13*y/8))
    return all(s in SEM and total-s in SEM for total, s in values)


def canonical(t):
    return min(t, t[1:]+t[:1], t[2:]+t[:2])


def classification(t):
    signature = {}
    short = []
    for p, q in zip(t, t[1:]+t[:1]):
        delta = sub(q, p)
        sq = norm(delta)
        assert sq.denominator == 1
        ell = isqrt(sq.numerator)
        assert ell*ell == sq
        h, rot = DIRS[direction(delta)]
        signature[h] = signature.get(h, 0)+ell*(-1)**rot
        if ell != 13:
            short.append(h)
    assert len(short) == 2 and short[0] == short[1]
    h = short[0]
    sign = signature[h]
    assert sign in (-1, 1)
    if signature.get(h+1):
        assert signature == {h: sign, h+1: -13*sign}
        group = 0 if sign == 1 else 1
    else:
        assert signature == {h: sign, h-1: -13*sign}
        group = 2 if sign == 1 else 3
    return h, group


def scaled_classification(t):
    """Check every stored triangle's pruning metadata using integer edges."""
    signature = {}
    short = []
    for p, q in zip(t, t[1:]+t[:1]):
        dx, dy = sub(q, p)
        size = isqrt(norm((dx, dy)))
        assert size*size == norm((dx, dy)) and size % D == 0
        ell = size//D
        divisor = gcd(dx, dy)
        h, rotation = DIRS[(dx//divisor, dy//divisor)]
        signature[h] = signature.get(h, 0)+ell*(-1)**rotation
        if ell != 13:
            short.append(h)
    assert len(short) == 2 and short[0] == short[1]
    h = short[0]
    sign = signature[h]
    assert sign in (-1, 1)
    if signature.get(h+1):
        assert signature == {h: sign, h+1: -13*sign}
        return h, 0 if sign == 1 else 1
    assert signature == {h: sign, h-1: -13*sign}
    return h, 2 if sign == 1 else 3


def reference_candidates(v, ray):
    dx, dy = ray
    z = isqrt(norm(ray))
    assert z*z == norm(ray)
    wx, wy = Q(dx, z), Q(dy, z)
    out = set()
    for ell, s, t in permutations((7, 8, 13)):
        x, y = Q(s*s+ell*ell-t*t-56, 2*ell), Q(56, ell)
        p = (v[0]+ell*wx, v[1]+ell*wy)
        q = (v[0]+wx*x-wy*y, v[1]+wx*y+wy*x+wy*y)
        if valid(p) and valid(q):
            tri = canonical((v, p, q))
            h, group = classification(tri)
            if -11 <= h <= 11:
                out.add((h, group, tri))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('geometry', type=Path)
    ap.add_argument('query_executable', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    with args.geometry.open() as inp:
        scale, npoints, ntriangles = map(int, inp.readline().split())
        assert scale == D
        points = [tuple(map(int, inp.readline().split())) for _ in range(npoints)]
        triangles = [tuple(map(int, inp.readline().split())) for _ in range(ntriangles)]
    for row in triangles:
        p, q, r = (points[i] for i in row[:3])
        sides = sorted(norm(sub(a, b)) for a, b in ((p, q), (q, r), (r, p)))
        assert sides == [49*D*D, 64*D*D, 169*D*D]
        a, b = sub(q, p), sub(r, p)
        assert a[0]*b[1]-a[1]*b[0] == 56*D*D
        assert all(v[1] >= 0 and 8*v[0] >= 7*v[1]
                   and 8*v[0]+15*v[1] <= 1232*D for v in (p, q, r))
        assert scaled_classification((p, q, r)) == row[3:5]
    rng = random.Random(634154)
    queries = []
    for row in rng.sample(triangles, min(600, len(triangles))):
        corner = rng.randrange(3)
        p, q = points[row[corner]], points[row[(corner+1) % 3]]
        ray = direction(sub(q, p))
        queries.append((p, ray))
    request = ''.join(f'{p[0]} {p[1]} {d[0]} {d[1]}\n' for p, d in queries)
    proc = subprocess.run([str(args.query_executable)], input=request, text=True,
                          capture_output=True, check=True)
    lines = proc.stdout.splitlines()
    assert len(lines) == len(queries)
    total = 0
    for (p, ray), line in zip(queries, lines):
        nums = list(map(int, line.split()))
        ct = nums[0]
        assert len(nums) == 1+8*ct
        actual = set()
        for i in range(ct):
            h, group, *coords = nums[1+8*i:1+8*(i+1)]
            t = tuple((Q(coords[2*j], D), Q(coords[2*j+1], D)) for j in range(3))
            assert classification(t) == (h, group)
            actual.add((h, group, canonical(t)))
        reference = reference_candidates(tuple(Q(x, D) for x in p), ray)
        assert actual == reference, (p, ray, actual, reference)
        total += ct
    report = {'status': 'PASS', 'all_generated_triangles_checked': len(triangles),
              'all_triangle_height_and_signed_groups_checked': len(triangles),
              'candidate_queries': len(queries), 'candidate_templates_compared': total,
              'methods': ['independent Fraction six-side-permutation generation',
                          'exact full tile-boundary Laurent signatures',
                          'all stored triangles: sides, positive area, containment'],
              'search_exhaustion_verified': False, 'N154_decided': False}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
