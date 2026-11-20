"""Separate exact checks of the edge signs, cyclic fold, smoothing and bounds."""
from collections import Counter
from fractions import Fraction as F
from itertools import accumulate
from math import gcd
from random import Random

from boundary import shape
from cycles import bound, projection
from directions import verify_directions


def delta(table, k, v):
    table[k] += v
    if table[k] == 0:
        del table[k]


def signs(d, e, b):
    # Coordinates (t,h). Endpoints of oriented intervals are counted directly
    # from polygons with counterclockwise boundary, without a transport formula.
    R, W = F(d*d, b), F(d*e, b)
    polygons = [([(0, 0), (b, 0), (b-R, W), (-R, W)], True),
                ([(0, 0), (W, -F(e*e,b)), (W, b-F(e*e,b)), (0, b)], False)]
    for vertices, horizontal in polygons:
        slants, slice_edges = Counter(), Counter()
        for (t, h), (s, y) in zip(vertices, vertices[1:]+vertices[:1]):
            if t == s:
                delta(slice_edges, t % W, h-y)
            elif h != y:
                sign = 1 if t > s else -1
                delta(slants, min(t,s), sign)
                delta(slants, max(t,s), -sign)
        expected = Counter()
        if horizontal:
            for pos, sign in [(-R,-1), (b-R,1), (0,1), (b,-1)]:
                delta(expected, pos, sign)
        assert slants == expected and not slice_edges


def shift(xs, step):
    return [xs[(i-step) % len(xs)] for i in range(len(xs))]


def diff(xs, step):
    return [x-y for x,y in zip(xs, shift(xs, step))]


def isum(xs, step, length):
    return [sum(xs[(i-step*j) % len(xs)] for j in range(length)) for i in range(len(xs))]


def check_fold(d, e, b, u, v, rng):
    # Arbitrary integer cycle counts and an arbitrary cut row, including wraps.
    size = d*e
    atoms = [0]*size
    for _ in range(min(300, size)):
        atoms[rng.randrange(size)] += rng.randrange(1, 4)
    last = rng.randrange(-2*d, 2*d)
    row = [atoms[(last*b+i*d) % size] for i in range(e)]
    def fold(xs):
        return [sum(xs[(j*b+i*d) % size] for j in range(last-d+1,last+1)) for i in range(e)]
    kappa = d*pow(b, -1, e) % e
    # R=d²/b on the circle of length de/b.
    assert (d*d-b*d*kappa) % size == 0
    assert fold(diff(diff(atoms,b),kappa*d)) == diff(diff(row,b),kappa)
    # Cancelling the two differences gives exactly the transport kernel in (5).
    kernel = isum(isum(row, 1, kappa), 1, b)
    assert diff(diff(kernel, 1), 1) == diff(diff(row,b),kappa)
    smoothed = isum(kernel,kappa,v)
    short = isum(isum(row,1,u),1,b)
    assert len(set(x-y for x,y in zip(smoothed,short))) == 1
    assert sum(short) == sum(row)*b*u


def slow_price(a,b,c,v,outer,axis_x):
    # Rebuild the source without (1-T) arrays or a residue histogram. The
    # baseline is the signed number of source points at or before each i.
    d,e = (c,a) if outer == axis_x else (a,c)
    n=a-b
    starts = list(range(c)) if outer else list(range(1,n+1))
    baseline = [sum(j % e <= i for j in starts) for i in range(e)]
    baseline = [c-t if outer else t-n for t in baseline]
    kap=next(t for t in range(1,e) if (b*t-d) % e == 0)
    levels = [sum(baseline[(i-j*kap)%e] for j in range(v)) for i in range(e)]
    return min(sum((t+h) % d for t in levels) for h in range(d))


def check_sizes():
    checked = 0
    for u in range(3,71):
        for v in range(1,u):
            if gcd(u,v) != 1 or u*u-v*v <= v*(2*u+v):
                continue
            a,b,c,*_ = shape(u,v)
            n=a-b
            for outer,axis in [(True,True),(True,False),(False,True),(False,False)]:
                d, exact = projection(a,b,c,v,outer,axis)
                if outer:
                    twice_lower = a*a-(c-a)**2-a*v if axis else a*a-c*v
                else:
                    twice_lower = n*n-(d-n)**2-v*n
                assert 2*exact >= twice_lower
            checked += 1
    return checked


def main():
    verify_directions()
    rng = Random(634)
    for u,v in [(3,1),(4,1),(6,1),(10,1),(11,2),(14,3),(16,5)]:
        a,b,c,*_=shape(u,v)
        for d,e in [(a,c),(c,a)]:
            signs(d,e,b)
            check_fold(d,e,b,u,v,rng)
        for outer in (True,False):
            for axis in (True,False):
                assert slow_price(a,b,c,v,outer,axis)==projection(a,b,c,v,outer,axis)[1]
    assert bound(10,1)[2:] == (1041,315)
    assert bound(6,1)[2:] == (1140,650)
    assert bound(86,5)[2:] == (F(30085293861,25370),1084833)
    assert 3047 == 11*277
    checked = check_sizes()
    print(f'Twelve orientations verified. Polygon signs, row telescoping, nonnegative transport, and independent direct residue minima verified. All four integral estimates tested on {checked} primitive triples.')


if __name__ == '__main__':
    main()
