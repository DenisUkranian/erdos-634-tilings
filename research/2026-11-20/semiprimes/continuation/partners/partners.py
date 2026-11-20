"""Find the unique mixed F2 arithmetic partner of an odd prime.

The public function expects a proven prime greater than three. All arithmetic
is integral. Run the module directly to replay the independent finite checks.
"""
from math import gcd, isqrt


def quadratic_root_three(p):
    """Tonelli-Shanks for a prime p with (3/p)=1."""
    if p % 4 == 3:
        return pow(3, (p + 1) // 4, p)
    odd, exponent = p - 1, 0
    while odd % 2 == 0:
        odd //= 2
        exponent += 1
    nonresidue = 2
    while pow(nonresidue, (p - 1) // 2, p) == 1:
        nonresidue += 1
    factor = pow(nonresidue, odd, p)
    root = pow(3, (odd + 1) // 2, p)
    residue = pow(3, odd, p)
    while residue != 1:
        i, power = 0, residue
        while power != 1:
            i += 1
            power = power * power % p
        correction = pow(factor, 1 << (exponent - i - 1), p)
        root = root * correction % p
        factor = correction * correction % p
        residue = residue * factor % p
        exponent = i
    return root


def product(z, w):
    x, y = z
    a, b = w
    return x * a + 3 * y * b, x * b + y * a


def principal_generator(p):
    r = quadratic_root_three(p)
    assert (r * r - 3) % p == 0
    dividend, divisor = (p, 0), (r, 1)
    while divisor != (0, 0):
        x, y = dividend
        a, b = divisor
        denom = a * a - 3 * b * b
        real = (2 * (x * a - 3 * y * b) + denom) // (2 * denom)
        imag = (2 * (y * a - x * b) + denom) // (2 * denom)
        dx, dy = product(divisor, (real, imag))
        dividend, divisor = divisor, (x - dx, y - dy)
    assert abs(dividend[0] ** 2 - 3 * dividend[1] ** 2) == p
    return dividend


def normalize(z, m):
    """Reduce a totally positive norm-m^2 element to (m, (2+sqrt(3))*m)."""
    x, y = z
    assert x > 0 and x * x - 3 * y * y == m * m
    while y <= 0:
        x, y = 2 * x + 3 * y, x + 2 * y
    while 2 * y > x:
        x, y = 2 * x - 3 * y, 2 * y - x
    assert 0 < y < m
    if x % 2:
        x, y = 2 * x - 3 * y, x - 2 * y
    assert x % 2 == 0 and y % 2 and 0 < y < m
    return x, y


def integer_partner(p):
    """Return Q whether prime, even or composite; return None for inert primes."""
    if p % 12 not in (1, 11):
        return None
    pi = principal_generator(p)
    x, y = normalize(product(pi, pi), p)
    q = (p + 3 * y) // 2
    assert x * x - 3 * y * y == p * p
    assert 3 * (x // 2) ** 2 == p * p - p * q + q * q
    return q


def primes_through(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = bytes([0, 0])
    for d in range(2, isqrt(limit) + 1):
        if sieve[d]:
            sieve[d * d::d] = bytes((limit - d * d) // d + 1)
    return [p for p in range(5, limit + 1) if sieve[p]]


def brute(m):
    result = []
    for y in range(1, m, 2):
        if gcd(m, y) == 1:
            square = m * m + 3 * y * y
            x = isqrt(square)
            if x * x == square:
                result.append((m + 3 * y) // 2)
    return result


if __name__ == '__main__':
    primes = primes_through(10000)
    for p in primes:
        q = integer_partner(p)
        assert brute(p) == ([] if q is None else [q])
    print('Direct comparison for', len(primes), 'primes from 5 through 10000: PASS')
    primes_set = set(primes)
    edges = {(p, integer_partner(p)) for p in primes}
    for p, q in edges:
        if q in primes_set:
            assert (q, p) in edges
    for p in (11, 13, 23, 47, 61, 73, 83, 97, 107, 167, 193):
        print(p, integer_partner(p))
    for m in range(5, 2001, 2):
        if m % 3 == 0:
            continue
        factors = [p for p in primes if m % p == 0]
        predicted = (1 << (len(factors) - 1)) if all(p % 12 in (1, 11) for p in factors) else 0
        assert len(brute(m)) == predicted
    print('All positive odd m coprime to 6 in [5,2000]: PASS')
