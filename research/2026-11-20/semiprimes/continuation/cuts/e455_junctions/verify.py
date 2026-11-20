"""Reconstruct and check the side-455 three-region exclusion using exact arithmetic."""
from collections import Counter
from fractions import Fraction as F
from functools import cache
from math import isqrt
from pathlib import Path
from subprocess import check_output, run
from tempfile import TemporaryDirectory

A, B, C = 35, 13, 43
L = A * B
VERTICES = ((0, 0), (L, 0), (0, L))


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def diff(p, q):
    return p[0] - q[0], p[1] - q[1]


def scale(t, p):
    return t * p[0], t * p[1]


def mul(p, q):
    x, y = p
    u, v = q
    return x*u - y*v, x*v + y*u + y*v


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


@cache
def unit(h, j):
    z = (F(A, C), F(B, C)) if h >= 0 else (F(A+B, C), F(-B, C))
    p = (1, 0)
    for _ in range(abs(h)):
        p = mul(p, z)
    for _ in range(j % 6):
        p = mul(p, (0, 1))
    return p


DIRECTIONS = {unit(h, j): (h, j) for h in range(-5, 6) for j in range(6)}
COINS = {0}
for amount in range(1, L+1):
    if any(amount-length in COINS for length in (A, B, C)):
        COINS.add(amount)


def edge(p, q):
    x, y = diff(q, p)
    squared = F(x*x + x*y + y*y)
    length = isqrt(squared.numerator)
    if squared != length*length or length not in COINS or length == 0:
        return None
    u = (F(x, length), F(y, length))
    return (length, *DIRECTIONS[u]) if u in DIRECTIONS else None


def mass(points):
    return F(sum(det(p, points[(i+1) % len(points)]) for i, p in enumerate(points)), A*B)


def orbit(edges):
    mirror = [(l, -h, (3-j) % 6) for l, h, j in reversed(edges)]
    keys = []
    for cycle in (list(edges), mirror):
        for i, (_, h, j) in enumerate(cycle):
            keys.append(tuple((l, t-h, (s-j) % 6) for l, t, s in cycle[i:] + cycle[:i]))
    return min(keys)


def from_edges(edges):
    points = []
    p = (0, 0)
    for l, h, j in edges:
        points.append(p)
        p = add(p, scale(l, unit(h, j)))
    assert p == (0, 0)
    return points


def chars_ok(points):
    m = mass(points)
    edges = [edge(p, points[(i+1) % len(points)]) for i, p in enumerate(points)]
    if not all(edges) or m <= 0 or m.denominator != 1:
        return False
    for t, w in ((0, A-B-C), (1, A-B+C)):
        s = sum(l*(-1 if (j+t*h) % 2 else 1) for l, h, j in edges)
        if s % w or (s//w-int(m)) % 2 or abs(s//w) > m:
            return False
    return True


def check_chords():
    # A chord's endpoints can be placed on the x and y sides by symmetry.
    # Include endpoints at the far vertices, skipping tangents and the whole board.
    offsets = [d for d in COINS if 0 < d <= L and L-d in COINS]
    for x in offsets:
        for y in offsets:
            if x == y == L or (x*y) % L:
                continue
            triangle = [(0,0), (x,0), (0,y)]
            if not chars_ok(triangle):
                continue
            remainder = [(x,0)] + ([(L,0)] if x<L else []) + [(0,L)]
            if y<L:
                remainder.append((0,y))
            assert not chars_ok(remainder)


def perimeter(p):
    x, y = p
    if y == 0:
        return x
    if x+y == L:
        return L+y
    assert x == 0
    return 3*L-y


def angular_coefficients(h, j):
    return next(((m, m+h) for m in range(j % 6, 7, 6)
                 if 0 <= m+h <= 6 and 0 < 2*m+h < 12), None)


def cells(line):
    x, y, d, *coords = map(int, line.split())
    center = (F(x, d), F(y, d))
    ends = [(F(coords[k], d), F(coords[k+1], d)) for k in (0, 2, 4)]
    shapes = []
    for i, p in enumerate(ends):
        q = ends[(i+1) % 3]
        off = lambda v: (perimeter(v)-perimeter(p)) % (3*L)
        between = sorted((v for v in VERTICES if 0 < off(v) < off(q)), key=off)
        points = [p, *between, q, center]
        assert chars_ok(points)
        edges = [edge(v, points[(k+1) % len(points)]) for k, v in enumerate(points)]
        for k, (_, h, j) in enumerate(edges):
            _, prev_h, prev_j = edges[k-1]
            if not angular_coefficients(prev_h-h, prev_j+3-j):
                return None
        shapes.append(orbit(edges))
    return tuple(sorted(shapes))


# Each boundary edge has types given by the vertex labels at its start and end.
LENGTHS = (A, B, C)
ANGLES = ((1, 0), (0, 1), (2, 2))
TYPES = [(i,j) for i in range(3) for j in range(3) if i != j]


@cache
def boundary_possible(shape):
    points = from_edges(shape)
    def inside(p):
        return all(det(unit(h, j), diff(p, points[k])) >= 0
                   for k, (_, h, j) in enumerate(shape))
    corners = []
    words = []
    for k, (length, h, j) in enumerate(shape):
        p = points[k]
        _, prev_h, prev_j = shape[k-1]
        mmax, nmax = angular_coefficients(prev_h-h, prev_j+3-j)
        allowed = set()
        def fan(m, n, first, last):
            if (m, n) == (mmax, nmax):
                allowed.add((last, first))
                return
            old = unit(h+n-m, j+m)
            for i, (dm, dn) in enumerate(ANGLES):
                M, N = m+dm, n+dn
                if M>mmax or N>nmax:
                    continue
                new = unit(h+N-M, j+M)
                for u, v in TYPES:
                    if i in (u, v):
                        continue
                    if inside(add(p, scale(LENGTHS[u], old))) and inside(add(p, scale(LENGTHS[v], new))):
                        fan(M, N, (i,v) if first is None else first, (u,i))
        fan(0, 0, None, None)
        corners.append(allowed)
        reached = [set() for _ in range(length+1)]
        for offset in range(length):
            if offset and not reached[offset]:
                continue
            start = add(p, scale(offset, unit(h,j)))
            for i, t in TYPES:
                length_here = LENGTHS[3-i-t]
                end = offset+length_here
                if end>length:
                    continue
                dm, dn = ANGLES[i]
                tip = add(start, scale(LENGTHS[t], unit(h+dn-dm, j+dm)))
                if not inside(tip):
                    continue
                if offset == 0:
                    reached[end].add(((i,t),(i,t)))
                else:
                    for first, (_, old) in reached[offset]:
                        if all(x+y<=3 for x,y in zip(ANGLES[old],ANGLES[i])):
                            reached[end].add((first,(i,t)))
        words.append(reached[length])
    for initial in TYPES:
        last = {initial}
        for corner, word in zip(corners, words):
            first = {q for p,q in corner if p in last}
            last = {q for p,q in word if p in first}
        if initial in last:
            return True
    return False


def check_small(shape, tiles, odd_signed, even_signed, high_residue):
    pts = from_edges(shape)
    assert mass(pts) == tiles
    # High arc comprises the two h=0 sides. Closing it by its chord yields its residue.
    i = next(i for i, (_,h,_) in enumerate(shape) if h == 0 and shape[i-1][1] < 0)
    p, q, r = [pts[(i+t) % len(pts)] for t in range(3)]
    displacement = mul(diff(r,p),(7,-1))
    # L_{-1} = c*z^{-1} / eta * R. Membership is tested by multiplication by eta*z/c.
    uv = mul(displacement, unit(1,0))
    assert all(F(v,C).denominator == 1 for v in uv)
    assert int(det(diff(q,p),diff(r,p)))*pow(L,-1,C) % C == high_residue
    G = sum(l*(-1 if j%2 else 1) for l,h,j in shape)//(A-B-C)
    H = sum(l*(-1 if (h+j)%2 else 1) for l,h,j in shape)//(A-B+C)
    assert (G-H)//2 == odd_signed and (G+H)//2 == even_signed
    low_residue = (tiles-high_residue) % C
    assert low_residue + high_residue + 2*C > tiles
    counts = [(n,tiles-n) for n in range(low_residue,tiles+1,C)
              if (tiles-n-high_residue)%C==0 and (n-odd_signed)%2==0
              and (tiles-n-even_signed)%2==0]
    if tiles == 65:
        assert not counts
    else:
        assert counts == [(14,77)]
        upper_positive = (14+odd_signed)//2
        b_counts = [j for i in range(7) for j in range(18)
                    if 35*i+13*j<=221 and (221-35*i-13*j)%43==0]
        assert min(b_counts)==5>upper_positive==2
        assert (221,-1,1) in shape


def main():
    check_chords()
    with TemporaryDirectory() as tmp:
        exe = str(Path(tmp)/'enumerate')
        run(['c++','-std=c++17','-O2',str(Path(__file__).with_name('enumerate.cpp')),'-o',exe],check=True)
        lines = check_output([exe],text=True).splitlines()
    configurations = {p for line in lines if (p:=cells(line)) is not None}
    survivors = [p for p in configurations if all(boundary_possible(s) for s in p)]
    assert len(lines)==42 and len(configurations)==7 and len(survivors)==2
    key = lambda s: int(mass(from_edges(s)))
    cases = {tuple(sorted(map(key,p))):p for p in survivors}
    for areas,args in [((65,117,273),(65,-9,-4,27)),((91,156,208),(91,-10,-3,34))]:
        check_small(min(cases[areas],key=key),*args)
    print('0 chords; 42 junctions; 7 shape triples; 5 boundary exclusions; 2 arithmetic exclusions.')


if __name__=='__main__':
    main()
