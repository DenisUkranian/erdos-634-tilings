"""Verify an exact packing with two translated, concave quadrilateral holes on the 5063 board."""
import gzip
import json
from collections import Counter, defaultdict
from math import gcd, isqrt
from pathlib import Path

DEN = 43


def diff(p, q):
    return p[0]-q[0], p[1]-q[1]


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def norm(p):
    x, y = p
    return x*x+x*y+y*y


def sides(points):
    return zip(points, points[1:]+points[:1])


def area(points):
    return sum(det(p,q) for p,q in sides(points))


def check(data):
    board = data['board']
    holes = data['holes']
    tiles = data['tiles']
    assert data['denominator'] == DEN
    assert board == [[0,0],[1079*DEN,0],[0,2135*DEN]]
    assert sorted(norm(diff(p,q)) for p,q in sides(board)) == [
        (k*DEN)**2 for k in (1079,1849,2135)]
    assert len(holes) == 2 and len(tiles) == 4373
    assert all(len(h) == 4 and area(h) == 345*35*13*DEN**2 for h in holes)
    shift = diff(holes[1][0],holes[0][0])
    assert all(diff(q,p) == shift for p,q in zip(*holes))
    assert holes[0] == [[35217,0],[46397,0],[30212,32025],[35217,13545]]
    # The opposite pair of sides at the bottom have disjoint y-ranges.
    # The side from B to C stays strictly to the right of the vertical
    # segment D to A throughout their common y-range. The quadrilateral is simple.
    A,B,C,D = holes[0]
    assert min(C[1],D[1]) > max(A[1],B[1]) and A[0] == D[0]
    assert det(diff(C,B),diff(A,B))>0 and det(diff(C,B),diff(D,B))>0
    for t in tiles:
        assert len(t)==3 and area(t)==35*13*DEN**2
        assert sorted(norm(diff(p,q)) for p,q in sides(t))==[(k*DEN)**2 for k in (13,35,43)]
    events = defaultdict(Counter)
    def boundary(points, sign):
        for p,q in sides(points):
            x,y=diff(q,p)
            d=gcd(x,y)
            u,v=x//d,y//d
            if (u,v)<(0,0):
                u,v=-u,-v
            key = (u,v,u*p[1]-v*p[0])
            events[key][tuple(p)] += sign
            events[key][tuple(q)] -= sign
    for polygon in tiles+holes:
        boundary(polygon,1)
    boundary(board,-1)
    assert all(not any(line.values()) for line in events.values())
    print('4373 verified tiles + two translated 345-tile quadrilaterals = 5063 tile areas.')
    print('Hole sides:', [isqrt(norm(diff(q,p)))//DEN for p,q in sides(holes[0])])


if __name__=='__main__':
    with gzip.open(Path(__file__).with_name('placements345.json.gz'),'rt') as f:
        check(json.load(f))
