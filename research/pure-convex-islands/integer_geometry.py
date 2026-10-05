#!/usr/bin/env python3
"""Integer geometry primitives for the stepped-surface verifier."""


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def area2(poly):
    return sum(p[0]*q[1]-p[1]*q[0]
               for p, q in zip(poly, poly[1:]+poly[:1]))


def rotate(p):
    return (-p[1], p[0]+p[1])


def signature(poly):
    anchor = min(map(tuple, poly))
    return tuple(sorted((p[0]-anchor[0], p[1]-anchor[1]) for p in poly))


def overlap(p, q):
    # Separating-axis theorem, with equality permitting boundary contact.
    for poly in (p, q):
        for u, v in zip(poly, poly[1:]+poly[:1]):
            nx, ny = u[1]-v[1], v[0]-u[0]
            pp = [nx*x+ny*y for x, y in p]
            qq = [nx*x+ny*y for x, y in q]
            if max(pp) <= min(qq) or max(qq) <= min(pp):
                return False
    return True

