#!/usr/bin/env python3
"""Finite exact checks of map, height, threshold and density formulas.

The universal Mordell-Weil and density conclusions are written proofs;
this checker does not certify a rank or a complete rational-point basis.
"""
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt, lcm
import json


def square_part(n):
    d, s, p = 1, 1, 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        d *= p ** (e % 2)
        s *= p ** (e // 2)
        p += 1
    d *= n
    return d, s


def finite_odd_density(basis):
    delta = Fraction(0)
    for size in range(1, len(basis) + 1):
        for subset in combinations(basis, size):
            delta += Fraction((-1) ** (size + 1), lcm(*subset))
    modulus = 2 * lcm(*basis)
    actual = sum(any(m % s == 0 for s in basis)
                 for m in range(1, modulus + 1, 2))
    assert delta == Fraction(actual, modulus // 2)
    return str(delta)


def main():
    if not __debug__:
        raise SystemExit('Assertions required; run without -O.')
    triples, seen = 0, {}
    for a in range(1, 501):
        for b in range(1, 501):
            if gcd(a, b) != 1:
                continue
            c = isqrt(a * a + a * b + b * b)
            if c * c != a * a + a * b + b * b:
                continue
            D = 3 * (a + b) * (a + 2 * b)
            d, s = square_part(D)
            assert d * s * s == D
            x = Fraction(3 * d * b, a + b)
            y = Fraction(9 * d * (a + 2 * b) * c, s * (a + b))
            assert y * y == x * x * x + (3 * d) ** 3
            assert 0 < x < 3 * d and y > 0
            recovered = x / (3 * d)
            assert (recovered.denominator - recovered.numerator,
                    recovered.numerator) == (a, b)
            key = (d, x)
            assert key not in seen or seen[key] == (a, b, c)
            seen[key] = (a, b, c)
            H = max(abs(x.numerator), x.denominator)
            assert H * H < 3 * d ** 3 * s * s
            A, B = max(a, b), min(a, b)
            assert (2*c-2*A-B) * (2*c+2*A+B) == 3*B*B
            assert 2*c-2*A-B >= 1
            assert 4*A < 3*B*B
            assert 16*A**4 < 3*d*s*s*B**4
            T = (3 * (A // B + 2) + 1) // 2
            assert Fraction(T) <= Fraction(3*A, 2*B) + 4
            if T > 4:
                assert 256 * (T-4)**4 <= 243 * d * s*s
            triples += 1
    densities = {str(b): finite_odd_density(b) for b in
                 [(3,), (3, 9, 15, 21), (15, 21, 33), (9, 15, 25, 35)]}
    print(json.dumps({
        'status': 'PASS',
        'primitive_ordered_triples_with_a_b_at_most_500': triples,
        'elliptic_map_injectivity_height_and_tail_checks': triples,
        'finite_odd_relative_density_checks': densities,
        'scope': 'finite identities only; see written infinite proof',
        'full_Erdos634_solved': False,
    }, indent=2))


if __name__ == '__main__':
    main()
