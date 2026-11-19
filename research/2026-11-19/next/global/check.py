"""Exact finite checks for the norm rotations and the 8p row."""

import json
from fractions import Fraction
from math import exp, gcd, isqrt, log, pi, sqrt


def sieve(limit):
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            for n in range(p * p, limit + 1, p):
                is_prime[n] = 0
    return [p for p, flag in enumerate(is_prime) if flag]


def test_rotations():
    output = []
    for d, a, b, denominator, k in (
        (2, 9, 4, 7, 77), (3, 14, 3, 13, 65),
        (2, 9, 4, 7, 91), (3, 14, 3, 13, 91),
    ):
        m = k // denominator
        assert a * a - d * b * b == denominator**2 and m * denominator == k
        original_low, original_high = Fraction(1, k), 1 - Fraction(1, k - 1)
        assert original_low < Fraction(d * b, a) < original_high
        low, high = Fraction(1, m), 1 - Fraction(1, m - 1)
        values = []
        for r in (0, original_low, original_high, 1):
            r = Fraction(r)
            rotated = abs(a * r - d * b) / (a - b * r)
            assert low <= rotated <= high
            values.append(str(rotated))
        direct, rotated = 0, 0
        for f in range(1, 400):
            for e in range(f + 1):
                n = d * f * f - e * e
                if k * e >= f and (k - 1) * (f - e) >= f:
                    x, y, mult = e, f, k
                    direct += 1
                else:
                    x, y, mult = abs(a * e - d * b * f), a * f - b * e, m
                    rotated += 1
                g = gcd(x, y)
                x, y, mult = x // g, y // g, mult * g
                assert 0 < x < y
                assert mult * x >= y and (mult - 1) * (y - x) >= y
                assert mult**2 * (d * y * y - x * x) == k * k * n
        output.append(dict(D=d, K=k, endpoints=values, direct=direct, rotated=rotated))
    return output


def norm_primes(d, n, primes):
    rest, exponent3 = n, 0
    for p in primes:
        if p * p > rest:
            break
        exponent = 0
        while rest % p == 0:
            rest //= p
            exponent += 1
        if p == 3:
            exponent3 = exponent
        if exponent % 2 and inert(d, p):
            return False
    if rest > 1 and inert(d, rest):
        return False
    if rest == 3:
        exponent3 = 1
    return d == 2 or (-1)**(exponent3 + 1) * (n // 3**exponent3) % 3 == 1


def inert(d, p):
    return (p % 8 in (3, 5)) if d == 2 else (p % 12 in (5, 7))


def test_norm_criterion(limit):
    primes = sieve(isqrt(limit) + 1)
    data = {}
    for d in (2, 3):
        reps = {d * y * y - x * x
                for y in range(1, isqrt(limit // (d - 1)) + 1)
                for x in range(y + 1)
                if d * y * y - x * x <= limit}
        arithmetic = {n for n in range(1, limit + 1) if norm_primes(d, n, primes)}
        assert arithmetic == reps
        data[d] = len(reps)
    return data


def nine_product_rows(n):
    witnesses = set()
    for scale in (1, 2):
        d = n // scale**2
        for v in range(2, isqrt(d) + 1):
            for u in range(1, v):
                if gcd(u, v) != 1:
                    continue
                b, q, p = v*v - u*u, 2*v*v - u*u, 3*v*v - u*u
                for name, value in (("alpha", b*q), ("Paliy", q*p)):
                    if value == d:
                        witnesses.add((name, u, v, 0, scale))
        for a in range(1, d + 1):
            for b in range(1, d // a + 1):
                if gcd(a, b) != 1:
                    continue
                for sign in (-1, 1):
                    c2 = a*a + sign*a*b + b*b
                    c = isqrt(c2)
                    if c*c != c2:
                        continue
                    eq = "equilateral120" if sign == 1 else "equilateral60"
                    if a < b and a*b == d:
                        witnesses.add((eq, a, b, c, scale))
                    if sign == 1:
                        for name, value in (
                            ("F1", b*(a+b)), ("iso120", b*(a+2*b)),
                            ("F2", (a+2*b)*(2*a+b)),
                            ("F3", 3*(a+2*b)*(a+b)), ("F4", (2*a+b)*(a+b)),
                        ):
                            if value == d:
                                witnesses.add((name, a, b, c, scale))
    return sorted(witnesses)


def test_eight_p():
    ps = [p for p in sieve(239 // 4) if p > 3 and p % 4 == 3]
    found = {8*p: nine_product_rows(8*p) for p in ps}
    assert {n: rows for n, rows in found.items() if rows} == {
        56: [("equilateral120", 7, 8, 13, 1)],
        88: [("F4", 3, 5, 7, 1)],
        184: [("iso120", 7, 8, 13, 1)],
    }
    return found


def constant_estimates():
    # Truncated positive products for illustration, not inputs to the proofs.
    primes = sieve(1000000)
    result = {}
    for d in (2, 3):
        ramified = {2} if d == 2 else {2, 3}
        l1 = log(1 + sqrt(2)) / sqrt(2) if d == 2 else log(2 + sqrt(3)) / sqrt(3)
        logarithm = log(l1 / pi)
        for p in primes:
            if p in ramified:
                logarithm += log(1 - 1 / p)
            else:
                logarithm += (1 if inert(d, p) else 2) * log(1 - 1 / p**2)
        result[d] = exp(logarithm / 2)
    geometric = (pi*pi / 6 - 1.25) * (1.5 * result[2] + result[3])
    return dict(A2=result[2], A3=result[3],
                nonclassical_contribution=geometric,
                total_lower_constant=geometric + 0.7642236535892206)


if __name__ == "__main__":
    print(json.dumps(dict(rotations=test_rotations(),
                          kernel_counts_through_20000=test_norm_criterion(20000),
                          eight_p_product_shapes=test_eight_p(),
                          approximate_constants=constant_estimates()), indent=2))
