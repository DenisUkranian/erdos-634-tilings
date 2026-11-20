"""Certify saturation of a specified packing by exact rational geometry."""
from fractions import Fraction
from itertools import chain
from pathlib import Path

F = Fraction

def minus(p, q):
    return p[0]-q[0], p[1]-q[1]

def plus(p, q):
    return p[0]+q[0], p[1]+q[1]

def times(k, p):
    return k*p[0], k*p[1]

def det(p, q):
    return p[0]*q[1]-p[1]*q[0]

def product(p, q):
    return p[0]*q[0]-p[1]*q[1], p[0]*q[1]+p[1]*(q[0]+q[1])

def edges(poly):
    return zip(poly, poly[1:]+poly[:1])

def area(poly):
    return sum(det(p,q) for p,q in edges(poly))

def convex_hull(points):
    def half(sequence):
        out = []
        for p in sequence:
            while len(out) >= 2 and det(minus(out[-1],out[-2]),minus(p,out[-1])) <= 0:
                out.pop()
            out.append(p)
        return out
    points = sorted(set(points))
    return half(points)[:-1]+half(reversed(points))[:-1]

def clip(poly, direction, threshold):
    result = []
    for x, y in edges(poly):
        k, h = det(direction,x)-threshold, det(direction,y)-threshold
        if k >= 0:
            result.append(x)
        if k*h < 0:
            result.append(plus(x,times(k/(k-h), minus(y,x))))
    return result

def free_translation(hull, obstacles, tile):
    # Translation positions first satisfy all supporting lines of the outer hull.
    allowed = hull
    for p, q in edges(hull):
        v = minus(q,p)
        bound = det(v,p)-min(det(v,t) for t in tile)
        allowed = clip(allowed,v,bound)
        if area(allowed) == 0:
            return False
    cells = [allowed]
    for obstacle in obstacles:
        forbidden = convex_hull(minus(p,t) for p in obstacle for t in tile)
        outside = []
        for cell in cells:
            for p, q in edges(forbidden):
                v = minus(q,p)
                bound = det(v,p)
                part = clip(cell,times(-1,v),-bound)
                if area(part) > 0:
                    outside.append(part)
                cell = clip(cell,v,bound)
                if area(cell) == 0:
                    break
        cells = outside
        if not cells:
            return False
    return True

def read_region():
    rows = Path(__file__).with_name("remaining_region.txt").read_text().splitlines()
    a,b,c,n = map(int,rows[0].split())
    polys = []
    for row in rows[1:]:
        k,*coords = map(int,row.split())
        p = [(F(x,c),F(y,c)) for x,y in zip(coords[::2],coords[1::2])]
        assert len(p) == k and area(p)>0 and len(convex_hull(p))==k
        polys.append(p)
    assert (a,b,c,n)==(33,7,37,len(polys)-1)
    return polys[0],polys[1:]

def check(scale=F(1), denominator=64):
    K,obstacles = read_region()
    shrink = scale*(1-F(18,denominator))
    for i in range(denominator):
        t = F(2*i+1,2*denominator)
        q = 1+t+t*t
        z = (1-t*t)/q,(2*t+t*t)/q
        for j in range(6):
            for apex in [(33,7),(40,-7)]:
                tile = [(0,0),times(33*shrink,z),times(shrink,product(z,apex))]
                assert not free_translation(K,obstacles,tile), (i,j,apex)
            z = -z[1],z[0]+z[1]
    print(f"Scale {scale}: all rotations in {denominator} intervals, both hands, every translation.")

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    check()
