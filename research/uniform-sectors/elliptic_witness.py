#!/usr/bin/env python3
"""Recover the large square-class-22 QP witness using exact curve arithmetic.

This is a single witness computation, not a rank/completeness calculation.
No floating-point arithmetic, network, or third-party dependency is used.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import gcd, isqrt
from typing import Optional, Tuple

Point = Optional[Tuple[Fraction, Fraction]]


def on_curve(point: Point, n: int) -> bool:
    if point is None:
        return True
    x, y = point
    return y * y == x * (x - 2 * n) * (x - 3 * n)


def add_points(left: Point, right: Point, n: int) -> Point:
    """Group law on y^2=x^3-5n*x^2+6n^2*x, including infinity."""
    if not isinstance(n, int) or n <= 0:
        raise ValueError("A positive integer curve parameter is required")
    if not on_curve(left, n) or not on_curve(right, n):
        raise ValueError("Input point is not on the curve")
    if left is None:
        return right
    if right is None:
        return left
    x, y = left
    X, Y = right
    if x == X and y == -Y:
        return None
    if left == right:
        slope = (3 * x * x - 10 * n * x + 6 * n * n) / (2 * y)
    else:
        slope = (Y - y) / (X - x)
    new_x = slope * slope + 5 * n - x - X
    answer = (new_x, slope * (x - new_x) - y)
    if not on_curve(answer, n):
        raise ArithmeticError("Group-law output failed the curve equation")
    return answer


def multiply(k: int, point: Point, n: int) -> Point:
    if not isinstance(k, int) or k < 0:
        raise ValueError("A nonnegative multiplier is required")
    answer = None
    while k:
        if k & 1:
            answer = add_points(answer, point, n)
        point = add_points(point, point, n)
        k //= 2
    return answer


def rational_square_root(value: Fraction) -> Fraction:
    if value < 0:
        raise ValueError("A nonnegative rational is required")
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    if a * a != value.numerator or b * b != value.denominator:
        raise ValueError("The rational is not a square")
    return Fraction(a, b)


def as_json(point: Point):
    if point is None:
        return None
    return [[c.numerator, c.denominator] for c in point]


def verify_witness() -> dict:
    n = 22
    seed = (Fraction(352, 9), Fraction(1936, 27))
    if not on_curve(seed, n):
        raise ArithmeticError("Seed is not on E_22")
    triple = multiply(3, seed, n)
    if triple is None or triple != add_points(add_points(seed, seed, n), seed, n):
        raise ArithmeticError("Tripling methods disagree")
    ratio = rational_square_root(triple[0] / n)
    u, v = ratio.numerator, ratio.denominator
    if not (0 < u < v and gcd(u, v) == 1):
        raise ArithmeticError("Recovered parameters are not a primitive tile")
    Q, P = 2 * v * v - u * u, 3 * v * v - u * u
    quotient = Fraction(Q * P, n)
    w = rational_square_root(quotient)
    if w.denominator != 1:
        raise ArithmeticError("The recovered multiplier is not integral")
    w = w.numerator
    if abs(triple[1]) != Fraction(n * n * u * w, v ** 3):
        raise ArithmeticError("Inverse map failed at y")
    if (u, v, w) != (10132, 22779, 248599631):
        raise ArithmeticError("Unexpected witness")
    if gcd(w, 6) != 1 or Q * P != n * w * w:
        raise ArithmeticError("Witness does not lie in the stated sector")
    # Additional exact group-law checks; these are tests, not a formalization.
    for a in range(6):
        for b in range(6):
            if multiply(a + b, seed, n) != add_points(multiply(a, seed, n), multiply(b, seed, n), n):
                raise ArithmeticError("Group-law regression failed")
    for root in (0, 2 * n, 3 * n):
        if add_points((Fraction(root), Fraction(0)), (Fraction(root), Fraction(0)), n) is not None:
            raise ArithmeticError("Two-torsion check failed")
    return {
        "status": "PASS", "curve_n": n, "curve": "y^2=x(x-2n)(x-3n)",
        "seed": as_json(seed), "seed_u_v": [4, 3], "seed_is_valid_triangle_pair": False,
        "triple": as_json(triple), "u": u, "v": v, "Q": Q, "P": P,
        "square_multiplier": w, "tile_count": Q * P,
        "group_law_regression_pairs": 36, "two_torsion_checks": 3,
        "scope": "One exact constructive witness; no rank, minimality, or point-completeness claim"
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = verify_witness()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
