#!/usr/bin/env python3
"""Supplementary finite checks; universal argument is the accompanying proof."""
from itertools import combinations
from math import isqrt, prod
import json

def prime(n):
    return n > 1 and all(n % q for q in range(2, isqrt(n) + 1))

def symbol(a, p):
    value = pow(a % p, (p - 1) // 2, p)
    return -1 if value == p - 1 else value

qualifying = [p for p in range(13, 3000, 24)
              if prime(p) and pow(3, (p - 1) // 4, p) == 1]
root_checks = []
for p in range(13, 3000, 24):
    if not prime(p):
        continue
    eps = pow(3, (p - 1) // 4, p)
    eps = -1 if eps == p - 1 else eps
    roots = [r for r in range(p) if (r*r + 6*r - 3) % p == 0]
    assert len(roots) == 2
    assert all(symbol(r, p) == -eps for r in roots)
    assert symbol(-3, p) == 1
    assert symbol(2, p) == -1 and symbol(3, p) == 1
    root_checks.append(p)

partitions = 0
products_checked = 0
first = qualifying[:10]
for length in (1, 3, 5, 7, 9):
    for primes in combinations(first, length):
        R = prod(primes)
        assert R % 8 == 5 and (6*R) % 16 == 14
        products_checked += 1
        for mask in range(1 << length):
            a_primes = [p for i, p in enumerate(primes) if mask >> i & 1]
            b_primes = [p for i, p in enumerate(primes) if not mask >> i & 1]
            A, B = prod(a_primes), prod(b_primes)
            assert A * B == R
            left = prod(symbol(A, p) for p in b_primes)
            right = prod(symbol(B, p) for p in a_primes)
            assert left == right
            assert (-1)**len(a_primes) != (-1)**len(b_primes)
            possible = (all(symbol(A,p) == -1 for p in b_primes)
                        and all(symbol(B,p) == -1 for p in a_primes))
            assert not possible
            partitions += 1

assert qualifying[0] == 13
assert pow(3, (37-1)//4, 37) == 36, 'p37 is a control outside the theorem'
assert 6*13*109*181 == 1538862
print(json.dumps({
    'status': 'PASS',
    'prime_root_checks_through_3000': len(root_checks),
    'qualifying_primes_through_3000': qualifying,
    'odd_support_products_from_first_ten_primes': products_checked,
    'partitions_checked': partitions,
    'proof': 'PROOF.md',
    'scope': 'Finite checks support the universal symbolic proof; no rank computation.',
    'small_even_multipliers_classified': False,
    'full_Erdos634_solved': False
}, indent=2))
