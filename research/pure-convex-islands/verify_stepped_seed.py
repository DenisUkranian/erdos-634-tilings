#!/usr/bin/env python3
"""Exact geometric checks for the universal stepped seed.

Finite checks supplement the general construction proof; they do not replace it.
Uses only Python's standard library and integer arithmetic.
"""
import json
from math import isqrt
from integer_geometry import area2, cross, overlap


def hull(points):
    points = sorted(set(points))
    halves = []
    for seq in (points, list(reversed(points))):
        out = []
        for p in seq:
            while len(out) > 1 and cross(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        halves.append(out[:-1])
    return halves[0]+halves[1]


def project(p):
    x, y, z = p
    return z-y, y-x


def construct(a, b):
    assert a >= 3 and b >= 3
    assert a <= b*(b-1) and b <= a*(a-1)
    scale = a*b
    height = [[max((b*(i+1)+a-1)//a, (a*(j+1)+b-1)//b)
               for j in range(b)] for i in range(a)]
    facets = []

    def add(axis, vertices, boundary=False):
        poly = hull([project(p) for p in vertices])
        if len(poly) < 3:
            return
        assert area2(poly) > 0
        # Each face lives in its axis plane. Its grid sizes are the lengths
        # of the two sides of the correctly oriented c-paired tile.
        assert len({p[axis] for p in vertices}) == 1
        dims = ((None, b, a), (a, None, b), (b, a, None))[axis]
        for p in vertices:
            for k in range(3):
                if dims[k] is not None:
                    assert p[k] % dims[k] == 0
        facets.append(dict(axis=axis, boundary=boundary, vertices=vertices, poly=poly))

    for i in range(a):
        for j in range(b):
            h = scale*height[i][j]
            add(2, [(-i*scale, -j*scale, h), (-(i+1)*scale, -j*scale, h),
                    (-(i+1)*scale, -(j+1)*scale, h), (-i*scale, -(j+1)*scale, h)])
            if i:
                lo = scale*height[i-1][j]
                add(0, [(-i*scale, -j*scale, lo), (-i*scale, -(j+1)*scale, lo),
                        (-i*scale, -(j+1)*scale, h), (-i*scale, -j*scale, h)])
            if j:
                lo = scale*height[i][j-1]
                add(1, [(-i*scale, -j*scale, lo), (-(i+1)*scale, -j*scale, lo),
                        (-(i+1)*scale, -j*scale, h), (-i*scale, -j*scale, h)])
    for j in range(b):
        h = scale*height[0][j]
        add(0, [(0, -j*scale, a*a*j), (0, -(j+1)*scale, a*a*(j+1)),
                (0, -(j+1)*scale, h), (0, -j*scale, h)], True)
        h = scale*height[a-1][j]
        add(0, [(-a*scale, -j*scale, h), (-a*scale, -(j+1)*scale, h),
                (-a*scale, -(j+1)*scale, b*scale+a*a*(j+1)),
                (-a*scale, -j*scale, b*scale+a*a*j)], True)
    for i in range(a):
        h = scale*height[i][0]
        add(1, [(-i*scale, 0, b*b*i), (-(i+1)*scale, 0, b*b*(i+1)),
                (-(i+1)*scale, 0, h), (-i*scale, 0, h)], True)
        h = scale*height[i][b-1]
        add(1, [(-i*scale, -b*scale, h), (-(i+1)*scale, -b*scale, h),
                (-(i+1)*scale, -b*scale, a*scale+b*b*(i+1)),
                (-i*scale, -b*scale, a*scale+b*b*i)], True)
    return facets


def verify(a, b):
    norm = a*a+a*b+b*b
    assert isqrt(norm)**2 == norm
    s = a*b
    outer = [(0, 0), (s*(a+b), -s*b), (s*(a+2*b), s*(a-b)), (s*b, s*a)]
    facets = construct(a, b)
    pairs = 0
    for i, rec in enumerate(facets):
        poly = rec['poly']
        assert all(cross(u, v, p) >= 0 for p in poly
                   for u, v in zip(outer, outer[1:]+outer[:1]))
        for prev in facets[:i]:
            assert not overlap(poly, prev['poly'])
            pairs += 1
    assert sum(area2(rec['poly']) for rec in facets) == area2(outer)
    assert area2(outer)//(a*b) == 2*norm*a*b
    return dict(status='PASS', a=a, b=b, c=isqrt(norm), sidecounts=[s, s],
                facets=len(facets), exact_nonoverlap_checks=pairs,
                triangles_after_grid_subdivision=2*norm*a*b)


if __name__ == '__main__':
    print(json.dumps([verify(a, b) for a, b in [(3, 5), (5, 16), (8, 7)]], indent=2))
