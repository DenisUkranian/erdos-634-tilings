#!/usr/bin/env python3
"""Exhaustive integer candidate audit; positive geometry is a separate proof."""

from math import gcd, isqrt, prod
import json


def factor(n):
    out = []
    p = 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out.append((p, e))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out


def main():
    n = 573390
    factors = factor(n)
    assert factors == [(2, 1), (3, 2), (5, 1), (23, 1), (277, 1)]
    assert prod(p ** e for p, e in factors) == n
    assert n % 16 == 14 and dict(factors)[5] % 2 == 1
    scales = [m for m in range(1, isqrt(n) + 1) if n % (m * m) == 0]
    assert scales == [1, 3]
    assert n // 9 == 63710 and (n // 9) % 3 != 0
    divisor_bands = []
    candidates = []
    for m in scales:
        coefficient = n // (m * m)
        if coefficient % 3:
            continue
        product = coefficient // 3
        for s in range(1, isqrt(product) + 1):
            if product % s:
                continue
            t = product // s
            if not s < t < 2 * s:
                continue
            a, b = 2 * s - t, t - s
            square = t * t - 3 * s * t + 3 * s * s
            c = isqrt(square)
            divisor_bands.append((m, s, t))
            if c * c == square and gcd(a, b) == 1:
                candidates.append((m, a, b, c))
    assert divisor_bands == [(1, 345, 554)]
    assert candidates == [(1, 136, 209, 301)]
    a, b, c = 136, 209, 301
    assert a * a + a * b + b * b == c * c
    assert (c*c, c*(a+2*b), 3*b*(a+b)) == (90601, 166754, 216315)
    assert 3 * (a+b) * (a+2*b) == n
    large, small = max(a, b), min(a, b)
    assert small*c - large*large == -2745
    assert 3 * (a+b) * (2*a+b) == 497835 != n
    old_tail = (3 * (large // small + 2) + 1) // 2
    improved_equi_tail = 3 * ((c + small - 1) // small)
    assert old_tail == 5 and improved_equi_tail == 9
    for k in range(201):
        p = 15 + 1650*k
        a, b, c = 8*(p+2), p*p-16, p*p+4*p+16
        count = 6*p*(p+8)*(p*p+4*p-8)
        assert a < b and gcd(a, b) == 1
        assert a*a+a*b+b*b == c*c
        assert count == 3*(a+b)*(a+2*b)
        assert count % 16 == 14 and count % 25 == 15 and count % 11 == 4
        q = p-15
        assert a*c-b*b == -p*(q**3+37*q*q+355*q+183) < 0
    print(json.dumps({'status': 'PASS', 'count': n, 'factorization': factors,
          'primitive_candidates': candidates, 'infinite_family_samples': 201,
          'F3_only_uses_separate_isolation_theorem': True,
          'large_unit_certificate_expanded': False,
          'full_Erdos634_solved': False}, indent=2))


if __name__ == '__main__':
    main()
