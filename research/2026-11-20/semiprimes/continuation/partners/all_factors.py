"""Enumerate primitive F2 partners of any odd factor M > 1.

Python 3, standard library only. The proof is in PARTNERS.md.
"""
from argparse import ArgumentParser
from itertools import product
from math import gcd, isqrt


def multiply(z, w):
    x, y = z
    u, v = w
    return (x*u + 3*y*v, x*v + y*u)


def power(z, n):
    result = (1, 0)
    while n:
        if n % 2:
            result = multiply(result, z)
        z = multiply(z, z)
        n //= 2
    return result


def norm(z):
    x, y = z
    return x*x - 3*y*y


def factors(n):
    result = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            result.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        result.append((n, 1))
    return result


def root_three(p):
    """Tonelli--Shanks for 3 at an odd split prime."""
    odd = p-1
    s = 0
    while odd % 2 == 0:
        s += 1
        odd //= 2
    candidate = 2
    while pow(candidate, (p-1)//2, p) == 1:
        candidate += 1
    c = pow(candidate, odd, p)
    t = pow(3, odd, p)
    r = pow(3, (odd+1)//2, p)
    while t != 1:
        i = 1
        term = t*t % p
        while term != 1:
            i += 1
            term = term*term % p
        b = pow(c, 1 << (s-i-1), p)
        r = r*b % p
        c = b*b % p
        t = t*c % p
        s = i
    assert r*r % p == 3
    return r


def prime_generator(p):
    """Euclidean gcd of p and r + sqrt(3), where r^2 = 3 mod p."""
    a, b = (p, 0), (root_three(p), 1)
    while b != (0, 0):
        d = norm(b)
        h, k = multiply(a, (b[0], -b[1]))
        if d < 0:
            d, h, k = -d, -h, -k
        q = ((2*h+d)//(2*d), (2*k+d)//(2*d))
        u, v = multiply(b, q)
        rem = (a[0]-u, a[1]-v)
        assert abs(norm(rem)) < abs(norm(b))
        a, b = b, rem
    assert abs(norm(a)) == p
    return a


def partners(m):
    if m <= 1 or m % 2 == 0:
        raise ValueError("M must be odd and greater than 1")
    f = factors(m)
    if any(p % 12 not in (1, 11) for p, _ in f):
        return []
    generators = [power(prime_generator(p), 2*e) for p, e in f]
    rows = []
    for signs in product((1, -1), repeat=len(generators)-1):
        z = generators[0]
        for (x, y), sign in zip(generators[1:], signs):
            z = multiply(z, (x, sign*y))
        x, y = z
        assert x > 0 and norm(z) == m*m
        while y < 0:
            x, y = 2*x+3*y, x+2*y
        while 2*y > x:
            x, y = 2*x-3*y, 2*y-x
        assert 0 < y < m and 2*y < x
        if x % 2:
            x, y = 2*x-3*y, x-2*y
        a, b, c = y, (m-y)//2, x//2
        assert a + 2*b == m and gcd(a, b) == 1 and min(a,b,c) > 0
        assert a*a + a*b + b*b == c*c
        rows.append((a,b,c,2*a+b))
    assert len(set(rows)) == 2**(len(f)-1)
    return sorted(rows)


def direct(m):
    rows = []
    for b in range(1, (m+1)//2):
        a = m - 2*b
        sq = a*a + a*b + b*b
        c = isqrt(sq)
        if gcd(a,b) == 1 and c*c == sq:
            rows.append((a,b,c,2*a+b))
    return sorted(rows)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("M", type=int, nargs="*")
    parser.add_argument("--verify-through", type=int)
    args = parser.parse_args()
    if args.verify_through is not None:
        for m in range(3, args.verify_through+1, 2):
            assert partners(m) == direct(m), m
        print("Direct enumeration agrees for every odd M from 3 through", args.verify_through)
    for m in args.M:
        print(m, partners(m))
