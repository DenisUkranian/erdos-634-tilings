"""Check the lower bounds without using the C++ placement algorithm."""
from fractions import Fraction as Q
from itertools import combinations
from math import gcd, isqrt

DIRECTIONS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
CASES = (
    ((5, 3, 7), 15, (1, 1, 2, 2, 2, 4, 1, 1, 2), (39, -55)),
    ((33, 7, 37), 193, (3, 1, 14, 6, 3, 25, 3, 2, 11), (511, -1551)),
    ((35, 13, 43), 432, (5, 4, 16, 11, 6, 29, 6, 2, 13), (1079, -2135)),
)


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def scale(t, u):
    return t*u[0], t*u[1]


def cross(u, v):
    return u[0]*v[1] - u[1]*v[0]


def side(u, v, w):
    return cross(sub(v, u), sub(w, u))


def ring_product(u, v):
    return u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0]+u[1]*v[1]


def edges(points):
    return list(zip(points, points[1:] + points[:1]))


def segments_meet(a, b, c, d):
    if any(max(min(a[i], b[i]), min(c[i], d[i])) >
           min(max(a[i], b[i]), max(c[i], d[i])) for i in range(2)):
        return False
    return side(a,b,c)*side(a,b,d) <= 0 and side(c,d,a)*side(c,d,b) <= 0


def certify(shape, k, lengths, rotation):
    a, b, c = shape
    p, q = a+2*b, 2*a+b
    assert c*c == a*a+a*b+b*b and gcd(a,b)==1
    point = (0, 0)
    polygon = []
    totals = [0]*6
    for index, length in enumerate(lengths):
        if length:
            polygon.append(point)
            totals[index % 6] += length
            point = add(point, scale(length, DIRECTIONS[index % 6]))
    assert point == (0,0) and totals[:3] == totals[3:]
    sides = edges(polygon)
    assert sum(cross(u,v) for u,v in sides) == 2*k
    assert sum(side(polygon[i-1],u,v)<0 for i,(u,v) in enumerate(sides)) == 1
    for i,j in combinations(range(len(sides)),2):
        if j-i not in (1,len(sides)-1):
            assert not segments_meet(*sides[i], *sides[j])

    x,y = rotation
    squared = x*x+x*y+y*y
    denom = isqrt(squared)
    assert denom*denom == squared
    rotated = [scale(Q(1,denom),ring_product(rotation,v)) for v in polygon]
    z = Q(a,c), Q(b,c)
    board = [(Q(0),Q(0)), (Q(c),Q(0)), scale(Q(a*p,c),ring_product(z,z))]
    # Intersect two contact equations in the translation plane. For each trial
    # translation, explicitly test every polygon vertex against all three sides.
    constraints = []
    for u,v in edges(board):
        dx,dy = sub(v,u)
        for w in rotated:
            constraints.append((-dy,dx,-side(u,v,w)))
    for (h,i,j),(l,m,n) in combinations(constraints,2):
        determinant = h*m-i*l
        if determinant == 0:
            continue
        shift = (Q(j*m-i*n,determinant), Q(h*n-j*l,determinant))
        if all(side(u,v,add(w,shift)) >= 0 for u,v in edges(board) for w in rotated):
            print(f'{p*q}: K={k}, one reflex vertex, translation=({shift[0]}, {shift[1]})')
            return
    raise AssertionError('no certified translation')


if __name__ == '__main__':
    for case in CASES:
        certify(*case)
