#!/usr/bin/env python3
"""Arithmetic replay for NO_PHASE_GAPS.md; geometric proof is in the note."""

from math import gcd
import json


def check(a, b, c, expected_n, expected_j, expected_limit, outside):
    assert gcd(a, b) == 1
    assert a * a + a * b + b * b == c * c
    n = (a + 2 * b) * (2 * a + b)
    assert n == expected_n
    assert n == 2 * c * c + 3 * a * b < 3 * c * c
    j = n % c
    assert j == expected_j > 0
    no_gap_limit = (n - j) // (2 * c)
    limit = (n - j - c) // (2 * c)
    assert limit == expected_limit
    assert 2 * c * limit + j + c <= n < 2 * c * (limit + 1) + j + c
    assert outside == j + 4 * c
    remote_limit = limit - 2
    assert remote_limit == (n - outside - c) // (2 * c)
    assert 2 * c * remote_limit + outside + c <= n
    assert 2 * c * (remote_limit + 1) + outside + c > n
    return {
        "N": n,
        "tile": [a, b, c],
        "core_residue": j,
        "required_node_limit_no_gaps_only": no_gap_limit,
        "required_node_limit_with_signed_parity": limit,
        "attachment_remote_outside_bound": outside,
        "attachment_remote_required_node_limit": remote_limit,
    }


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    cases = [
        check(33, 7, 37, 3431, 27, 45, 175),
        check(35, 13, 43, 5063, 32, 58, 204),
    ]
    assert [r["attachment_remote_required_node_limit"] for r in cases] == [43, 56]
    print(json.dumps({
        "scope": "Necessary population bounds; neither whole board is decided.",
        "cases": cases,
    }, indent=2))

