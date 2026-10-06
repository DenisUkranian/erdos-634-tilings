#!/usr/bin/env python3
"""Finite exact arithmetic audit of the square-class-38 elliptic orbit.

This is not a proof of infinitude or of a geometric tiling construction.
The proof and its separate geometric inputs are documented in
docs/infinite-minimal-multipliers.md. No construction module is imported.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path


if not __debug__:
    raise SystemExit("Run without -O/-OO: this audit uses assertions.")

K = 114
D = 38
F = Fraction
Point = tuple[Fraction, Fraction] | None
# Coefficients (a2, a4, a6) of y^2 = x^3 + a2*x^2 + a4*x + a6.
E = (0, 0, K**3)
CURVE_F = (6 * K, -3 * K**2, 0)
Q: Point = (F(-110), F(388))
G: Point = (F(54), F(216))


def on_curve(curve: tuple[int, int, int], point: Point) -> bool:
    if point is None:
        return True
    x, y = point
    a2, a4, a6 = curve
    return y * y == x**3 + a2 * x * x + a4 * x + a6


def neg(point: Point) -> Point:
    return None if point is None else (point[0], -point[1])


def add(curve: tuple[int, int, int], p: Point, q: Point) -> Point:
    assert on_curve(curve, p) and on_curve(curve, q)
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    xx, yy = q
    a2, a4, _ = curve
    if x == xx and y == -yy:
        return None
    if p == q:
        slope = (3 * x * x + 2 * a2 * x + a4) / (2 * y)
    else:
        assert x != xx
        slope = (yy - y) / (xx - x)
    new_x = slope * slope - a2 - x - xx
    result = (new_x, -y + slope * (x - new_x))
    assert on_curve(curve, result)
    return result


def phi(point: Point) -> Point:
    """E -> F, with the ordinate sign used in the written proof."""
    assert on_curve(E, point)
    if point is None or point == (F(-K), F(0)):
        return None
    x, y = point
    t = x + K
    result = (y * y / (t * t), y * (3 * K * K - t * t) / (t * t))
    assert on_curve(CURVE_F, result)
    return result


def dual(point: Point) -> Point:
    """F -> E; in particular dual(G)=-Q and dual(-G)=Q."""
    assert on_curve(CURVE_F, point)
    if point is None or point == (F(0), F(0)):
        return None
    x, y = point
    result = (
        y * y / (4 * x * x) - K,
        y * (-3 * K * K - x * x) / (8 * x * x),
    )
    assert on_curve(E, result)
    return result


def valuation(value: int | Fraction, prime: int) -> int:
    value = F(value)
    assert value != 0, "Use in_neighborhood for a vanishing difference."
    numerator = abs(value.numerator)
    denominator = value.denominator
    result = 0
    while numerator % prime == 0:
        result += 1
        numerator //= prime
    while denominator % prime == 0:
        result -= 1
        denominator //= prime
    return result


def divisible_locally(value: Fraction, prime: int, exponent: int) -> bool:
    return value == 0 or valuation(value, prime) >= exponent


def normalize(point: Point) -> dict[str, int | bool]:
    """Check the exact normalization, including outside the positive cone."""
    assert point is not None and on_curve(E, point)
    x, y = point
    C = isqrt(x.denominator)
    assert C * C == x.denominator and C > 0
    A = x.numerator
    ordinate = y * C**3
    assert ordinate.denominator == 1
    B = ordinate.numerator
    assert gcd(A, C) == gcd(B, C) == 1
    W_squared = A + K * C * C
    assert W_squared > 0
    W = isqrt(W_squared)
    assert W * W == W_squared and gcd(W, C) == 1
    assert B % W == 0
    V = B // W
    assert V * V == A * A - K * A * C * C + K * K * C**4
    g = gcd(K, A)
    assert g == gcd(K * C * C - A, A) and V % g == 0
    assert (3 * W * C) % g == 0
    s = 3 * W * C // g
    a, b, c = (K * C * C - A) // g, A // g, abs(V) // g
    assert gcd(a, b) == 1 and c * c == a * a + a * b + b * b
    assert 3 * (a + 2 * b) * (a + b) == D * s * s
    positive = 0 < x < K
    if positive:
        assert min(a, b, c) > 0
        assert a + b > c and a + c > b and b + c > a
    return {
        "A": A, "B": B, "C": C, "W": W, "g": g,
        "a": a, "b": b, "c": c, "s": s, "positive": positive,
    }


def f3_candidates(multiplier: int) -> list[tuple[int, int, int, int]]:
    """Complete tiny inverse search for s|multiplier; no cutoff inference."""
    result = []
    for s in range(1, multiplier + 1):
        if multiplier % s:
            continue
        coefficient = D * s * s
        if coefficient % 3:
            continue
        product = coefficient // 3
        for lower in range(1, isqrt(product) + 1):
            if product % lower:
                continue
            upper = product // lower
            if not lower < upper < 2 * lower or gcd(lower, upper) != 1:
                continue
            a, b = 2 * lower - upper, upper - lower
            square = a * a + a * b + b * b
            c = isqrt(square)
            if c * c == square:
                result.append((s, a, b, c))
    return result


def run() -> dict:
    assert on_curve(E, Q) and on_curve(CURVE_F, G)
    assert dual(G) == neg(Q) and dual(neg(G)) == Q
    assert phi(Q) == (F(9409), F(945071))
    assert phi(None) is None and dual(None) is None
    assert phi((F(-K), F(0))) is None
    assert dual((F(0), F(0))) is None
    assert add(E, Q, neg(Q)) is None
    assert add(CURVE_F, G, neg(G)) is None
    # Arithmetic part of the Lutz--Nagell certificate, not a proof of that theorem.
    discriminant = -432 * K**6
    assert 388 % 97 == 0 and discriminant % 97 != 0
    base = normalize(Q)
    assert tuple(base[key] for key in ("A", "C", "W", "g", "s")) == (-110, 1, 2, 2, 3)

    positive_indices = []
    bad_valuations = []
    neighborhood_matches = {prime: 0 for prime in (2, 3, 19)}
    good_primes = (5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 43)
    good_implications = 0
    records = []
    point_e = point_f = None
    max_multiplier_digits = 0
    for n in range(1, 16):
        point_e = add(E, point_e, Q)
        point_f = add(CURVE_F, point_f, G)
        assert point_e is not None and point_f is not None
        assert dual(neg(point_f)) == point_e
        # Both dual compositions, checked on these fifteen finite samples.
        assert dual(phi(point_e)) == add(E, point_e, point_e)
        assert phi(dual(point_f)) == add(CURVE_F, point_f, point_f)
        assert phi(point_e) == neg(add(CURVE_F, point_f, point_f))
        x, y = point_e
        assert (point_f[1] / (2 * point_f[0])) ** 2 == x + K
        data = normalize(point_e)
        s = data["s"]
        assert isinstance(s, int)
        if data["positive"]:
            positive_indices.append(n)
        max_multiplier_digits = max(max_multiplier_digits, len(str(s)))
        bad_valuations.append({
            "n": n,
            "v2": valuation(s, 2),
            "v3": valuation(s, 3),
            "v19": valuation(s, 19),
        })
        for prime, exponent, expected in ((2, 3, 0), (3, 1, 1), (19, 1, 0)):
            if valuation(x, prime) >= 0 and divisible_locally(x + 110, prime, exponent):
                neighborhood_matches[prime] += 1
                assert valuation(s, prime) == expected
                assert valuation(data["C"], prime) == 0
                if prime == 2:
                    assert valuation(data["W"], 2) == valuation(data["g"], 2) == 1
                else:
                    assert valuation(data["W"], prime) == valuation(data["g"], prime) == 0
        for prime in good_primes:
            if valuation(x, prime) >= 0 and valuation(x + K, prime) == 0:
                good_implications += 1
                assert valuation(s, prime) == 0
                assert all(valuation(data[key], prime) == 0 for key in ("C", "W", "g"))
        records.append({
            "n": n,
            "E": [[z.numerator, z.denominator] for z in point_e],
            "F": [[z.numerator, z.denominator] for z in point_f],
            "normalization": data,
        })
    assert positive_indices == [7, 9, 10, 12]
    assert not f3_candidates(1) and not f3_candidates(3)
    pairs_114 = [(114 // v, v) for v in range(1, isqrt(114) + 1) if 114 % v == 0]
    assert pairs_114 == [(114, 1), (57, 2), (38, 3), (19, 6)]
    assert all(not v < u < 2 * v for u, v in pairs_114)
    residues_19 = {r * r % 19 for r in range(19)}
    assert 2 not in residues_19 and 3 not in residues_19
    for u in range(16):
        for v in range(16):
            if (v * v - u * u) * (2 * v * v - u * u) % 16 == 6:
                assert v % 2 == 1 and u % 4 == 2
                assert ((2 * v * v - u * u) // 2) % 8 == 7
    assert all(kernel % 8 != 7 for kernel in (1, 19))
    digest = sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "status": "PASS",
        "full_Erdos634_solved": False,
        "format": "ERDOS634_CLASS38_FINITE_ORBIT_AUDIT_V1",
        "arithmetic": "Python standard library integers and fractions.Fraction",
        "sample_indices": {"first": 1, "last": 15, "count": 15},
        "dual_orbit_equalities_checked": 15,
        "dual_compositions_checked": 30,
        "square_lifts_and_normalizations_checked": 15,
        "positive_primitive_F3_indices": positive_indices,
        "maximum_sample_multiplier_decimal_digits": max_multiplier_digits,
        "bad_prime_multiplier_valuations": bad_valuations,
        "local_neighborhood_implications_checked": {
            str(prime): count for prime, count in neighborhood_matches.items()
        },
        "good_prime_unit_implications_checked": good_implications,
        "base_formal_multiplier": 3,
        "negative_F3_multiplier_checks": {"1": "no candidate", "3": "no candidate"},
        "factor_pairs_114": pairs_114,
        "quadratic_nonresidues_mod_19": [2, 3],
        "alpha_residue_implication_mod_16": "PASS",
        "lutz_nagell_discriminant_arithmetic": "97 divides ordinate; 97 does not divide discriminant",
        "exact_sample_data_sha256": digest,
        "scope": "Finite arithmetic audit only; not an infinitude proof, geometric certificate, or full solution of problem 634.",
        "proof": "../../docs/infinite-minimal-multipliers.md",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", "--output", dest="report", type=Path,
                        help="Optionally write this finite report to the given JSON file.")
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
