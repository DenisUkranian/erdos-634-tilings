"""Independent exact verifier for the unrestricted 136 certificate; standard library only."""
from bisect import bisect_left, bisect_right
from fractions import Fraction
from functools import cache
from gzip import open as gzip_open
from itertools import permutations
from json import load
from math import gcd
from pathlib import Path

WEIGHTS = Path(__file__).resolve().parents[1] / "alpha" / "unrestricted136.json.gz"


@cache
def slope(dx, dy):
    divisor = gcd(dx, dy)
    if dx < 0 or (dx == 0 and dy < 0):
        divisor = -divisor
    return dx // divisor, dy // divisor


def oriented_area(a, b, c):
    return (b[0]-a[0]) * (c[1]-a[1]) - (b[1]-a[1]) * (c[0]-a[0])


def main():
    with gzip_open(WEIGHTS, "rt") as stream:
        cert = load(stream)
    charges = cert["endpoints"]
    axis_count = max(abs(h) for _, _, h, _ in charges)
    scale = 32 * 3 ** (axis_count + 26)
    denominator = cert["endpoint_denominator"]
    assert scale % denominator == scale % cert["packing_denominator"] == 0
    mass = cert["mass_weight"]
    assert mass > 0

    rotation = {}
    x, y = Fraction(1), Fraction(0)
    for k in range(axis_count + 1):
        for exponent, second in ((k, y), (-k, -y)):
            assert (scale*x).denominator == (scale*second).denominator == 1
            rotation[exponent] = int(scale*x), int(scale*second)
        x, y = (-x-35*y)/6, (x-y)/6
    weights = {}
    for x, y, h, value in charges:
        position = (x*(scale//denominator), y*(scale//denominator))
        key = position, slope(*rotation[h])
        assert key not in weights and value != 0
        weights[key] = value

    step = scale // cert["packing_denominator"]
    probes = sorted((x*step, y*step, v) for x,y,v in cert["packing"])
    assert all(v >= 0 for _,_,v in probes)
    probe_x = [x for x,_,_ in probes]

    # A boundary point must be a joint in the word of complete sides on that wall.
    reachable = {0}
    for i in range(137):
        if i in reachable:
            reachable.update(i+l for l in (3,8,9))
    def admissible(p):
        x,y = p
        if min(y, x-17*y, 136*scale-x-17*y) < 0:
            return False
        if y == 0:
            if x % scale or x//scale not in reachable or 136-x//scale not in reachable:
                return False
        if x == 17*y or 136*scale-x == 17*y:
            if (18*y) % scale or 18*y//scale not in reachable or 72-18*y//scale not in reachable:
                return False
        return True

    @cache
    def templates(h):
        # Only the designated unit edge direction is fixed. Enumerate the six
        # assignments of actual side lengths, both edge signs and both half-planes.
        triangles = set()
        ux,uy = rotation[h]
        for a,b,c in permutations((3,8,9)):
            for s in (-1,1):
                dx,dy = s*ux,s*uy
                adjacent = a*dx,a*dy
                projection = a*a + b*b - c*c
                for hand in (-1,1):
                    nx = projection*dx - hand*280*dy
                    ny = projection*dy + hand*8*dx
                    assert nx%(2*a)==0 and ny%(2*a)==0
                    other = nx//(2*a),ny//(2*a)
                    if oriented_area((0,0),adjacent,other)>0:
                        triangles.add((adjacent,other))
                    else:
                        triangles.add((other,adjacent))
        return triangles

    def edge_charge(triangle):
        value = 0
        for a,b in zip(triangle,triangle[1:]+triangle[:1]):
            key = slope(b[0]-a[0],b[1]-a[1])
            value += weights.get((a,key),0) - weights.get((b,key),0)
        return value

    outer = [(0,0),(136*scale,0),(68*scale,4*scale)]
    demand = edge_charge(outer)
    packing = sum(v for _,_,v in probes)
    all_positive = 0
    seen = set()
    for x,y,h,_ in charges:
        p = x*(scale//denominator), y*(scale//denominator)
        if not admissible(p):
            continue
        for (ux,uy),(vx,vy) in templates(h):
            b = p[0]+ux,p[1]+uy
            c = p[0]+vx,p[1]+vy
            if not admissible(b) or not admissible(c):
                continue
            triple = tuple(sorted((p,b,c)))
            if triple in seen:
                continue
            seen.add(triple)
            excess = edge_charge([p,b,c]) - mass
            if excess <= 0:
                continue
            # Interior probes can each be charged to at most one tile.
            lo,hi = min(p[0],b[0],c[0]),max(p[0],b[0],c[0])
            for px,py,w in probes[bisect_right(probe_x,lo):bisect_left(probe_x,hi)]:
                if all(oriented_area(s,t,(px,py))>0 for s,t in ((p,b),(b,c),(c,p))):
                    excess -= w
                    if excess <= 0:
                        break
            all_positive += max(0,excess)

    numerator = demand - packing - all_positive
    assert numerator > 136*mass
    print(f"charged endpoints {len(weights)}, placements {len(seen)}, packing points {len(probes)}")
    print(f"target {demand}, packing {packing}, positive excess {all_positive}")
    print(f"{numerator}/{mass} > 136; exact area ratio 136")


if __name__ == "__main__":
    main()
