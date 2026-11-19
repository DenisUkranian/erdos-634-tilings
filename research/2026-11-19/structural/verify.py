"""Reproduce the finite part of Theorem 1 using only Python's standard library."""

from collections import Counter
from math import gcd, isqrt
import json


def primes_to(bound):
    return [
        p for p in range(2, bound + 1)
        if all(p % j for j in range(2, isqrt(p) + 1))
    ]


def odd_valuation(number, prime):
    odd = False
    while number % prime == 0:
        odd = not odd
        number //= prime
    return odd


def product_rows(bound):
    """Yield every ordered primitive product-row record with coefficient <= bound."""
    for f in range(2, isqrt(bound) + 1):
        for e in range(1, f):
            if gcd(e, f) != 1:
                continue
            b, q, r = f*f-e*e, 2*f*f-e*e, 3*f*f-e*e
            for row, value in (("alpha", b*q), ("other-scalene", q*r)):
                if value <= bound:
                    yield row, value, (e, f)
    # Every listed coefficient is at least a*b. Use A >= s, then try both orders.
    for s in range(1, isqrt(bound) + 1):
        for big in range(s, bound // s + 1):
            if gcd(big, s) != 1:
                continue
            for sign in (-1, 1):
                c2 = big*big + sign*big*s + s*s
                c = isqrt(c2)
                if c*c != c2:
                    continue
                for a, b in sorted({(big, s), (s, big)}):
                    values = [("equilateral-" if sign == -1 else "equilateral+", a*b)]
                    if sign == 1:
                        values.extend([
                            ("F1", b*(a+b)), ("isosceles", b*(a+2*b)),
                            ("F2", (a+2*b)*(2*a+b)), ("F3", 3*(a+b)*(a+2*b)),
                            ("F4", (a+b)*(2*a+b)),
                        ])
                    for row, value in values:
                        if value <= bound:
                            yield row, value, (a, b, c)


def main():
    # Cubic bound p^3/64 >= 9p^2/5 begins at the first integer p >= 116.
    small = [p for p in primes_to(115) if p >= 19 and p % 24 in (5, 19)]
    assert small == [19, 29, 43, 53, 67, 101]
    bound = 9 * max(small)**2 // 5
    rows = list(product_rows(bound))
    assert len({row for row, _, _ in rows}) == 9
    assert ("other-scalene", 322, (2, 3)) in rows
    # Control outside the theorem's p-range: the same test must detect D=15,40.
    control = {d for _, d, _ in rows if 5*d < 9*5**2 and odd_valuation(d, 5)}
    assert control == {15, 40}
    examined = {}
    for p in small:
        candidates = [(row, d, sides) for row, d, sides in rows if 5*d < 9*p*p]
        hits = [r for r in candidates if odd_valuation(r[1], p)]
        assert not hits, (p, hits)
        examined[p] = {"primitive_records_examined": len(candidates), "hits": len(hits)}
    return {
        "finite_primes": examined,
        "largest_coefficient_examined": bound,
        "primitive_records_per_row_at_largest_bound": dict(sorted(Counter(r[0] for r in rows).items())),
        "control_p_5_coefficients": sorted(control),
    }


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    print(json.dumps(main(), indent=2))
