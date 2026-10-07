#!/usr/bin/env python3
"""Read-only exact arithmetic checks for the parameter-descent audit."""
from math import gcd, isqrt
import json


def divisors(n):
    low = [d for d in range(1, isqrt(n) + 1) if n % d == 0]
    return sorted(set(low + [n // d for d in low]))


def f3_replacements(n):
    out = []
    for s in divisors(n):
        t = n // s
        if not (s < t < 2 * s and gcd(s, t) == 1):
            continue
        q = t * t - 3 * s * t + 3 * s * s
        c = isqrt(q)
        if c * c == q:
            out.append((2 * s - t, t - s, c))
    return out


def main():
    assert divisors(1610) == [1, 2, 5, 7, 10, 14, 23, 35, 46,
                              70, 115, 161, 230, 322, 805, 1610]
    assert f3_replacements(1610) == [(24, 11, 31)]
    assert 4830 % 16 == 14
    assert 2 * 3 * 5 * 7 * 23 == 4830
    triples = set()
    for p in range(2, 101):
        for q in range(1, p):
            if gcd(p, q) != 1:
                continue
            a, b, c = p*p-q*q, q*(2*p+q), p*p+p*q+q*q
            if (p-q) % 3 == 0:
                a, b, c = a//3, b//3, c//3
            triples.add((a, b, c))
            triples.add((b, a, c))
    for a, b, c in triples:
        assert gcd(a, b) == 1 and c*c == a*a+a*b+b*b
        s, t = a+b, a+2*b
        n = s*t
        assert c*c == t*t-3*s*t+3*s*s
        X, Y = 3*s*s-n, 3*s*s*c
        assert Y*Y == X*X*X+n*n*n
        assert (b < a <= 2*b) == (4*s <= 3*t and 2*t < 3*s)
        assert (b < a <= 2*b) == (2*n < 3*s*s and 4*s*s <= 3*n)
        u, v = abs(a-b), c
        assert 0 < u < v and gcd(u, v) == 1
        assert (a+2*b)*(2*a+b) == 3*v*v-u*u
        A, B = max(a, b), min(a, b)
        assert B >= 3 and A >= 5
        threshold = (3*(A//B+2)+1)//2
        assert threshold <= A+1 <= c
    print(json.dumps({
        "status": "PASS",
        "primitive_ordered_samples": len(triples),
        "f3_4830_ordered_primitive_tiles": f3_replacements(1610),
        "full_Erdos634_solved": False,
        "scope": "Exact arithmetic only; no new tiling or non-tiling decision."
    }, indent=2))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O: verification uses assertions.")
    main()
