"""Count the two possible geometric branches in the squarefree split-prime sector."""
from functools import lru_cache
from math import gcd, isqrt, prod

from check_squarefree_mass import primes


def cube_root(n):
    low, high = 0, 1
    while high ** 3 <= n:
        high *= 2
    while high - low > 1:
        mid = (low + high) // 2
        if mid ** 3 <= n:
            low = mid
        else:
            high = mid
    return low


def census(limit):
    prime_list = primes(isqrt(limit) + 1)

    @lru_cache(maxsize=None)
    def allowed(n):
        for prime in prime_list:
            if prime * prime > n:
                break
            if n % prime == 0:
                n //= prime
                if n % prime == 0 or prime % 12 not in (1, 11):
                    return False
        return n == 1 or n % 12 in (1, 11)

    equilateral, f2, built = set(), set(), set()
    # For ordered plus-norm triples, ab > u**3*v/9.
    for v in range(1, isqrt(isqrt(9 * limit)) + 1, 2):
        for u in range(2 * v + 2, cube_root(9 * limit // v) + 1, 2):
            if gcd(u, v) > 1:
                continue
            g = gcd(3, u-v)
            a, b = (u*u-v*v)//g, v*(2*u+v)//g
            if a <= b:
                continue
            if a*b <= limit and a*b % 24 == 23 and allowed(a) and allowed(b):
                assert gcd(a, b) == 1
                equilateral.add(a*b)
            p, q = a+2*b, 2*a+b
            if p*q <= limit and allowed(p) and allowed(q):
                assert p*q % 24 == 23 and gcd(p,q) == 1
                f2.add(p*q)
                if u <= 4*v*(v-1 if g == 3 and v%3 == 2 else v):
                    built.add(p*q)
    return equilateral, f2, built


if __name__ == '__main__':
    for bound in (10**6, 10**8, 10**10):
        eq, f2, built = census(bound)
        print(f'X={bound}: equilateral candidates={len(eq)}, '
              f'F2 candidates={len(f2)}, staircase={len(built)}, '
              f'overlap={len(eq & f2)}, union outside staircase={len((eq | f2)-built)}')
    for prime in (5,7,17,19):
        count = sum(prod((v,u-v,u+v,2*u+v)) % prime == 0
                    for v in range(prime) for u in range(prime))
        assert count == 4*prime-3
    print('Four-line sieve counts checked directly at four forbidden primes.')
