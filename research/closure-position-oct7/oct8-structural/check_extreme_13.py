#!/usr/bin/env python3
"""Exact bounded arithmetic in EXTREME_13.md; no geometric search."""

from itertools import product
import json


def rot(a):
    return (-a[2], a[0], a[1])


def decompositions(total, choices):
    """All unordered decompositions into allowed nonzero line pairs."""
    out = []

    def visit(left, first, used):
        if left == (0, 0):
            out.append(tuple(used))
            return
        for i in range(first, len(choices)):
            p = choices[i]
            if p[0] <= left[0] and p[1] <= left[1]:
                visit((left[0] - p[0], left[1] - p[1]), i, used + [p])

    visit(total, 0, [])
    return out


def check():
    actual = set()
    for a in product(range(-13, 14), repeat=3):
        s = sum(abs(x) for x in a)
        if s > 13 or s % 2 != 1:
            continue
        currents = (8*a[0]+7*a[1], 8*a[1]+7*a[2], 8*a[2]-7*a[0])
        if all(x % 13 == 0 for x in currents):
            actual.add(a)
    predicted = set()
    for seed in ((13, 0, 0), (9, -1, 3), (6, -5, 2)):
        a = seed
        for _ in range(6):
            predicted.add(a)
            a = rot(a)
    assert len(actual) == 18 and actual == predicted
    assert all(sum(abs(x) for x in a) == 13 for a in actual)

    pairs = sorted((m, n) for m in range(14) for n in range(14-m)
                   if m+n and (8*m-7*n) % 13 == 0)
    expected = sorted(((13, 0), (0, 13), (9, 1), (5, 2), (1, 3),
                       (6, 5), (2, 6), (3, 9)))
    assert pairs == expected
    checks = []
    for rotation_counts, multiplicity, totals, line_bounds in (
        ((13, 0, 0), 13, ((13, 0), (0, 13)), (1, 1)),
        ((9, 3, 1), 9, ((9, 1), (3, 9)), (1, 3)),
        ((6, 2, 5), 5, ((5, 2), (6, 5)), (1, 2)),
    ):
        decomps = [decompositions(t, pairs) for t in totals]
        assert all(decomps)
        maxima = tuple(max(map(len, ds)) for ds in decomps)
        assert maxima == line_bounds
        assert multiplicity > maxima[0] * maxima[1]
        checks.append({"rotation_counts_0_2_4": rotation_counts,
                       "selected_orientation_multiplicity": multiplicity,
                       "supporting_line_pair_totals": totals,
                       "max_distinct_lines": maxima,
                       "max_gamma_vertices": maxima[0] * maxima[1],
                       "all_line_decompositions": decomps})
    return {"status": "PASS", "full_Erdos634_solved": False,
            "N154_solved": False, "odd_L1_kernel_vectors": 18,
            "possible_nonempty_line_pairs": pairs,
            "geometric_case_arithmetic": checks,
            "conclusion": "An extreme nonzero short height cannot contain exactly 13 tiles."}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
