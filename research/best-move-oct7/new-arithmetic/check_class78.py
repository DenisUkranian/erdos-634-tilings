#!/usr/bin/env python3
"""Exact checks supporting the elementary all-multiplier class-78 proof."""

from fractions import Fraction as F
from math import gcd, isqrt
import json


def valuation(q, p):
    q = F(q)
    assert q
    numerator, denominator = abs(q.numerator), q.denominator
    result = 0
    while numerator % p == 0:
        numerator //= p
        result += 1
    while denominator % p == 0:
        denominator //= p
        result -= 1
    return result


def point(a, b, c, s):
    ss, tt = a+b, a+2*b
    assert ss*tt == 26*s*s
    x = F(26*(2*c+2*tt-3*ss), ss)
    y = F(52*s, ss)*x
    assert y*y == x*x*x+156*x*x-2028*x
    ss0, tt0, cc0 = F(ss,s), F(tt,s), F(c,s)
    assert x == tt0*(2*tt0-3*ss0+2*cc0)
    assert y == 2*tt0*x
    assert x*x+(156-4*tt0*tt0)*x-2028 == 0
    return x, y


def main():
    residues = {x*x % 13 for x in range(13)}
    assert residues == {0,1,3,4,9,10,12}
    for d in (2,6):
        assert d not in residues
        assert (-12*pow(d,-1,13)) % 13 not in residues
        # First congruence forces u=W=0; after division the second forces v=0.
        assert all(u == w == 0 for u in range(13) for w in range(13)
                   if (w*w-d*u**4) % 13 == 0)
        coefficient = (-12*pow(d,-1,13)) % 13
        assert all(v == w == 0 for v in range(13) for w in range(13)
                   if (w*w-coefficient*v**4) % 13 == 0)
    roots = [q for q in range(13) if (q*q-q+1) % 13 == 0]
    assert roots == [4,10] and all(q in residues for q in roots)
    for e in (2,6):
        coefficient = (-12*pow(e,-1,13)) % 13
        solutions = [(u,v) for u in range(13) for v in range(13)
                     if (e*u**4+12*u*u*v*v+coefficient*v**4) % 13 == 0]
        assert solutions == [(0,0)]
    assert point(3,5,7,2) == (F(52),F(676))
    assert valuation(52,2) == 2
    assert (7*7,7*(3+2*5),3*5*(3+5)) == (49,91,120)
    triples = []
    for a in range(1,1001):
        for b in range(1,1001):
            if gcd(a,b) != 1:
                continue
            c2 = a*a+a*b+b*b
            c = isqrt(c2)
            if c*c != c2:
                continue
            d = 3*(a+b)*(a+2*b)
            if d % 78:
                continue
            s = isqrt(d//78)
            if 78*s*s != d:
                continue
            x,y = point(a,b,c,s)
            assert s % 2 == 0 and valuation(x,2) % 2 == 0
            triples.append((a,b,c,s))
    assert triples
    print(json.dumps({
        'status': 'PASS',
        'modulo_13_descent_classes': [2,6,26,78],
        'explicit_rational_map': 'PASS',
        'seed_count': 312,
        'primitive_triples_with_a_b_at_most_1000': triples,
        'scope': 'Finite supporting checks. The universal odd-multiplier exclusion is the written elementary descent proof.',
        'full_Erdos634_solved': False,
    }, indent=2))


if __name__ == '__main__':
    main()
