#!/usr/bin/env python3
"""Exact finite arithmetic check; infinite inputs are written in STRUCTURAL_AUDIT.md."""
import json
from math import gcd, isqrt


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def inverse_rows(z):
    prod = 114 * z * z
    rows = []
    for A in range(1, isqrt(prod) + 1):
        if prod % A:
            continue
        B = prod // A
        if A < B < 2 * A:
            a, b = 2 * A - B, B - A
            norm = a * a + a * b + b * b
            rows.append((z, A, B, a, b, gcd(a, b), norm))
    return rows


def forward_rows(z):
    # From A<B<2A and AB=prod, A<sqrt(prod); hence a,b<sqrt(prod).
    prod = 114 * z * z
    rows = []
    for a in range(1, isqrt(prod) + 1):
        for b in range(1, isqrt(prod) + 1):
            if (a + b) * (a + 2 * b) == prod:
                rows.append((z, a + b, a + 2 * b, a, b,
                             gcd(a, b), a * a + a * b + b * b))
    return sorted(rows)


def main():
    if not __debug__:
        raise SystemExit('Run without -O: assertions are part of this checker.')
    powers = {1}
    for p in range(3, 16, 2):
        if is_prime(p):
            z = p
            while z * z < 228:
                powers.add(z)
                z *= p
    assert powers == {1, 3, 5, 7, 9, 11, 13}
    rows = []
    for z in sorted(powers):
        inv = inverse_rows(z)
        assert inv == forward_rows(z)
        for row in inv:
            norm = row[-1]
            root = isqrt(norm)
            assert root * root < norm < (root + 1) ** 2
        rows.extend(inv)
    expected = [
        (3, 27, 38, 16, 11, 1, 553),
        (5, 38, 75, 1, 37, 1, 1407),
        (5, 50, 57, 43, 7, 1, 2199),
        (7, 57, 98, 16, 41, 1, 2593),
        (9, 81, 114, 48, 33, 3, 4977),
        (11, 114, 121, 107, 7, 1, 12247),
        (13, 114, 169, 59, 55, 1, 9751),
    ]
    assert rows == expected
    print(json.dumps({
        'status': 'PASS',
        'candidate_powers': sorted(powers),
        'complete_ratio_factor_rows': rows,
        'primitive_norm_witnesses': 0,
        'independent_forward_and_inverse_agree': True,
        'infinite_theorem_scope': 'written proof plus stated inputs',
        'full_Erdos634_solved': False,
    }, indent=2))


if __name__ == '__main__':
    main()
