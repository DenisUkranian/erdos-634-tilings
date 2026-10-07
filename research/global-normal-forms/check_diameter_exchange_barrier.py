#!/usr/bin/env python3
"""Exact supplemental checks of the scalar seam-length barrier."""
from math import gcd, isqrt
import json


def in_two_generator_semigroup(value, first, second):
    return any((value - k * first) % second == 0
               for k in range(value // first + 1))


def exchange_minimum(side, first, second, upper):
    for length in range(side, upper + 1, side):
        if in_two_generator_semigroup(length, first, second):
            return length
    raise AssertionError((side, first, second, upper))


def check_tile(a, b, c, plus):
    upper = a * b
    lengths = [exchange_minimum(a, b, c, upper),
               exchange_minimum(b, a, c, upper),
               exchange_minimum(c, a, b, upper)]
    assert lengths[0] <= upper and lengths[1] <= upper
    assert lengths[2] < upper
    targets = [(upper, upper, upper)]
    if plus:
        targets += [(a*b, b*c, b*(a+b)),
                    (b*c, b*c, b*(a+2*b)),
                    (a*(a+2*b), b*(2*a+b), c*c),
                    (c*c, c*(a+2*b), 3*b*(a+b)),
                    (a*c, b*(2*a+b), c*(a+b))]
    for target in targets:
        assert max(target) >= upper >= max(lengths)
    return lengths, len(targets)


def main():
    bound = 300
    counts = {"plus": 0, "minus": 0}
    target_checks = 0
    for a in range(2, bound + 1):
        for b in range(2, bound + 1):
            if gcd(a, b) != 1:
                continue
            for sign, name in [(1, "plus"), (-1, "minus")]:
                norm = a*a + sign*a*b + b*b
                c = isqrt(norm)
                if c*c != norm:
                    continue
                _, checked = check_tile(a, b, c, sign == 1)
                counts[name] += 1
                target_checks += checked
    examples = {}
    for a, b, c in [(24, 11, 31), (8, 7, 13)]:
        lengths, _ = check_tile(a, b, c, True)
        examples[f"{a},{b},{c}"] = lengths
    print(json.dumps({"status": "PASS", "short_side_bound": bound,
                      "ordered_primitive_triples": counts,
                      "target_checks": target_checks,
                      "exchange_minima_examples": examples,
                      "full_Erdos634_solved": False}, indent=2))


if __name__ == "__main__":
    main()
