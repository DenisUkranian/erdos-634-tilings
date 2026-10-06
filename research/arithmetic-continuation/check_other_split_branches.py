#!/usr/bin/env python3
"""Exact restricted-versus-direct arithmetic checks in four norm rows."""

import argparse
from functools import lru_cache
import json
from math import gcd, isqrt
from pathlib import Path

if not __debug__:
    raise SystemExit("Verification requires assertions; run without -O or PYTHONOPTIMIZE.")

ROWS = ("I120", "F2", "F3", "F4")


def factors(n):
    answer = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            answer[p] = answer.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        answer[n] = answer.get(n, 0) + 1
    return answer


def divisors(n):
    answer = [1]
    for p, exponent in factors(n).items():
        answer = [a * p ** e for a in answer for e in range(exponent + 1)]
    return sorted(answer)


def splitting(p):
    return p > 3 and pow(3, (p - 1) // 2, p) == 1


def split_part(m):
    answer = 1
    for p, exponent in factors(m).items():
        if splitting(p):
            answer *= p ** exponent
    return answer


def kernel_plus(d):
    answer = gcd(d, 2)
    for p in factors(d):
        if splitting(p):
            answer *= p
    return answer


def coefficient(row, a, b):
    return {"I120": b * (a + 2 * b),
            "F2": (a + 2 * b) * (2 * a + b),
            "F3": 3 * (a + 2 * b) * (a + b),
            "F4": (2 * a + b) * (a + b)}[row]


def norm_root(a, b):
    if a <= 0 or b <= 0 or gcd(a, b) != 1:
        return None
    squared = a * a + a * b + b * b
    c = isqrt(squared)
    return c if c * c == squared else None


@lru_cache(None)
def restricted_lists(d, h):
    answer = {row: set() for row in ROWS}
    for U in divisors(kernel_plus(d) * h * h):
        for r in range(1, (U - 1) // 2 + 1):
            a, b = U - 2 * r, r
            c = norm_root(a, b)
            if c is None:
                continue
            for row in ROWS:
                x, y = (b, a) if row == "F4" else (a, b)
                D = coefficient(row, x, y)
                if D % d:
                    continue
                s = isqrt(D // d)
                if s * s * d == D:
                    answer[row].add((x, y, c, s))
    return answer


def direct_list(row, d, m):
    answer = set()
    for s in divisors(m):
        D = d * s * s
        if row == "F3" and D % 3:
            continue
        product = D // 3 if row == "F3" else D
        for factor in divisors(product):
            other = product // factor
            if row == "I120":
                # Directly choose b, rather than the restricted factor U.
                a, b = other - 2 * factor, factor
            elif row == "F2":
                a3, b3 = 2 * other - factor, 2 * factor - other
                if a3 % 3 or b3 % 3:
                    continue
                a, b = a3 // 3, b3 // 3
            elif row == "F3":
                a, b = 2 * other - factor, factor - other
            else:
                a, b = factor - other, 2 * other - factor
            c = norm_root(a, b)
            if c is not None:
                assert coefficient(row, a, b) == D
                answer.add((a, b, c, s))
    return answer


def check():
    comparisons = {row: 0 for row in ROWS}
    positive_comparisons = {row: 0 for row in ROWS}
    distinct_witnesses = {row: set() for row in ROWS}
    for d in range(1, 151):
        if any(exponent != 1 for exponent in factors(d).values()):
            continue
        for m in range(1, 81):
            h = split_part(m)
            if h > 13:
                continue
            candidates = restricted_lists(d, h)
            for row in ROWS:
                restricted = {entry for entry in candidates[row] if m % entry[3] == 0}
                direct = direct_list(row, d, m)
                assert restricted == direct, (row, d, m, restricted, direct)
                comparisons[row] += 1
                positive_comparisons[row] += bool(direct)
                for a, b, c, s in direct:
                    distinct_witnesses[row].add((d, a, b, c, s))
                    U = 2 * a + b if row == "F4" else a + 2 * b
                    assert kernel_plus(d) * h * h % U == 0
                    assert coefficient(row, a, b) < 3 * U * U
                    A, B = max(a, b), min(a, b)
                    M = 3 * (A // B + 2)
                    bound = 15 if d == 1 else 12
                    assert s * M < bound * d * h ** 3

    # Four ordered-row checks using the same positive primitive norm tile.
    ordered_regressions = []
    for row in ROWS:
        a, b, c = (7, 8, 13) if row == "F4" else (8, 7, 13)
        D = coefficient(row, a, b)
        d = 1
        for p, exponent in factors(D).items():
            if exponent % 2:
                d *= p
        s = isqrt(D // d)
        m = 2 * s
        assert (a, b, c, s) in direct_list(row, d, m)
        assert (a, b, c, s) in restricted_lists(d, split_part(m))[row]
        ordered_regressions.append({"row": row, "d": d, "m": m,
                                    "witness": [a, b, c, s]})
    assert direct_list("F3", 110, 6) == {(8, 7, 13, 3)}
    assert (5, 3, 7, 2) in restricted_lists(66, 1)["F3"]
    return {"status": "PASS", "full_Erdos634_solved": False,
            "scope": "Arithmetic coefficient comparison; not small-scale geometric sufficiency",
            "comparisons_by_row": comparisons,
            "total_independent_comparisons": sum(comparisons.values()),
            "positive_comparisons_by_row": positive_comparisons,
            "distinct_witnesses_by_row": {row: len(entries)
                                           for row, entries in distinct_witnesses.items()},
            "ordered_even_multiplier_regressions": ordered_regressions,
            "kernel_max": 150, "multiplier_max": 80, "split_part_max": 13}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="write the arithmetic-check report here")
    args = parser.parse_args()
    output = json.dumps(check(), indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
