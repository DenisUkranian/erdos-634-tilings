"""Exact cross-check of the scale-one straight-cut theorem using angle triples."""
from fractions import Fraction
from functools import cache
from heapq import heappop, heappush
from itertools import product
from math import gcd, lcm


def multiply(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c + b * d


def semigroup_test(a, b, c):
    """Apéry distances modulo b from the two other generators."""
    distances = [None] * b
    distances[0] = 0
    queue = [(0, 0)]
    while queue:
        cost, residue = heappop(queue)
        if cost != distances[residue]:
            continue
        for length in (a, c):
            value = cost + length
            dest = value % b
            if distances[dest] is None or distances[dest] > value:
                distances[dest] = value
                heappush(queue, (value, dest))
    assert all(d is not None for d in distances)
    return lambda length: length >= distances[length % b]


def enumerate_caps(a, b, c, complement=False):
    A, B, C = a * (a + 2*b), b * (2*a + b), c*c
    axes = {(1, 1): (A, B), (2, 0): (B, C), (0, 2): (A, C)}
    if complement:
        # Allow reaching old vertices. The assertion below excludes even
        # an integral triangular cap whose chord is a board diagonal.
        L = A-c*(a+b)
        tail = c*(c-a)
        axes = {(1,1): (L,B), (2,3): (L,B), (1,2): (tail,B), (2,0): (tail,B)}
    in_semigroup = semigroup_test(a, b, c)
    alpha = Fraction(b, c), Fraction(a, c)
    beta = Fraction(a, c), Fraction(b, c)

    @cache
    def sine(pair):
        # y coordinate of the complex unit in the axial basis 1, exp(i*pi/3).
        unit = (1, 0)
        for factor, count in zip((alpha, beta), pair):
            for _ in range(count):
                unit = multiply(unit, factor)
        return unit[1]

    found = set()
    for apex, (left, right) in axes.items():
        for at_left in product(range(4-apex[0]), range(4-apex[1])):
            at_right = tuple(3-i-j for i, j in zip(apex, at_left))
            if (0, 0) in (at_left, at_right):
                continue
            sines = [sine(t) for t in (at_right, at_left, apex)]
            den = lcm(*(s.denominator for s in sines))
            raw = [int(s*den) for s in sines]
            common = gcd(*raw)
            x, y, chord = [s//common for s in raw]
            # Rotating or reflecting a triangle changes either boundary sum at
            # most by a sign. Initially its left-hand offset points along 1.
            coeffs = []
            for j in range(2):
                first_turn = (3-at_left[j]) % 2
                last_heading = (apex[j]+3) % 2
                coeffs.append(x + (-1)**first_turn * chord + (-1)**last_heading * y)
            units = (a-b-c, a-b+c)
            stride = lcm(*(abs(d)//gcd(abs(d),z) for d,z in zip(units,coeffs)))
            margin = 0 if complement else 1
            limit = min((left-margin)//x, (right-margin)//y)
            for t in range(stride, limit+1, stride):
                r, s, third = t*x, t*y, t*chord
                if not all(map(in_semigroup, (r,s,third,left-r,right-s))):
                    continue
                area = Fraction(r*s, a*b)*sine(apex)
                if area.denominator != 1:
                    continue
                signed = [t*f//d for f,d in zip(coeffs,units)]
                if not all(abs(z) <= area and (area-z)%2 == 0 for z in signed):
                    continue
                found.add((apex,r,s))
    return found


def test_board(u, v):
    g = gcd(3, u-v)
    a, b, c = (u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g
    assert gcd(a, b) == 1 and a >= 2*b and a*b%2 and a*a+a*b+b*b == c*c
    w, s = a+b, a*b
    expected = {((1,1),r,t) for r,t in
                ((s,s),(2*s,2*s),(s,b*w),(b*w,s),(2*b*w,2*s),(a*w,s))}
    if v > 1:
        expected.add(((0,2),c*w,a*c))
        assert u > 4*v*(v-1)
        h = b//v
        d = w-c
        H = d - (v-1)*h//2
        z = -H * pow(2, -1, v) % v
        x = H+z
        L = a*(a+2*b)-c*w
        y, rem = divmod(L-x*a-z*c, b)
        assert min(x,y,z) >= 0 and rem == 0
        assert not enumerate_caps(a, b, c, complement=True)
    found = enumerate_caps(a,b,c)
    assert found == expected, (u,v,found ^ expected)
    print(f"u={u} v={v} N={(a+2*b)*(2*a+b)} admissible_chords={len(found)}")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    for params in [(10,1),(6,1),(16,1),(12,1),(22,1),(18,1),(40,1),
                   (44,3),(122,5),(268,7)]:
        test_board(*params)
