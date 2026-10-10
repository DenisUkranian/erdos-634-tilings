#!/usr/bin/env python3
"""Finite regression for the conditional 2p W-reduction theorem.

This is not a proof of the infinite theorem. The mathematical proof is in
W_DOUBLE_PRIME_REDUCTION.md. Only Python standard library is required.
"""
from math import gcd, isqrt


def is_prime(n):
    if n < 2:
        return False
    for q in range(2, isqrt(n) + 1):
        if n % q == 0:
            return False
    return True


def candidates(p):
    n = 2 * p
    rows = []
    for v in range(2, isqrt(n) + 1):
        u2 = 2 * v * v - n
        if not 0 < u2 < v * v:
            continue
        u = isqrt(u2)
        if u * u == u2 and gcd(u, v) == 1:
            rows.append((u, v))
    return rows


def main():
    checked = 0
    for p in range(7, 100_001, 8):
        if not is_prime(p):
            continue
        rows = candidates(p)
        assert len(rows) == 1, (p, rows)
        u, v = rows[0]
        assert u % 2 == 0 and v % 2 == 1 and 0 < u < v
        assert v*v - 2*(u//2)**2 == p
        checked += 1
    found = []
    for k in range(1, 101):
        p = 8*k*k - 1
        if is_prime(p):
            rows = candidates(p)
            assert rows == [(4*k-2, 4*k-1)], (k,p,rows)
            u, v = rows[0]
            assert v*(v*v-u*u) < 2*v*v
            found.append((k,p,2*p))
    print('Every prime p ≡ 7 mod 8 up to 100000 has exactly one W scale-one candidate.')
    print('Prime cases checked:', checked)
    print('First conditional global exclusions (k, p=8k²−1, N=2p):')
    for row in found[:14]: print(*row)
    print('PASS: prime-sector finite regression')

if __name__ == '__main__':
    main()
