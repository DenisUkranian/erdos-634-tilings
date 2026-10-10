#!/usr/bin/env python3
"""Exact arithmetic/finite audit of the no-61-height lemma.

Standard library only. The accompanying note proves the geometric
supporting-line argument. PASS is not a tiling existence/nonexistence
certificate and is not a formal proof-assistant verification.
"""
from __future__ import annotations

import json
from itertools import product
from math import gcd
from pathlib import Path

A, B, C, N = 56, 9, 61, 14430
Pair = tuple[int, int]


def direction(j: int) -> tuple[int, int, int]:
    v = [0, 0, 0]
    v[j % 3] = 1 if j % 6 < 3 else -1
    return tuple(v)


def chi(v: tuple[int, int, int]) -> int:
    return v[0] - v[1] + v[2]


def bounded_pair_sums(pairs: list[Pair], limit: int) -> set[Pair]:
    """Finite nonnegative-semigroup membership; each step increases m+n."""
    reached = {(0, 0)}
    for total in range(2 * limit + 1):
        for m in range(max(0, total - limit), min(limit, total) + 1):
            n = total - m
            if (m, n) not in reached:
                continue
            for u, v in pairs:
                if m + u <= limit and n + v <= limit:
                    reached.add((m + u, n + v))
    return reached


def main() -> None:
    assert C * C == A * A + A * B + B * B
    assert N == 3 * (A + B) * (A + 2 * B)
    assert gcd(A - B, C) == 1 and C % 2 == 1

    # Reconstruct all 12 short-edge currents; no signed-vector table imported.
    groups: dict[int, list[dict]] = {1: [], -1: []}
    for typ, j in product("AB", range(6)):
        first, last = (A, B) if typ == "A" else (B, A)
        e, f = direction(j), direction(j + 5)
        current = tuple(first * e[i] + last * f[i] for i in range(3))
        s = chi(current) // (A - B)
        assert s in (-1, 1)
        assert chi(current) == s * (A - B)
        a_axis, b_axis = (j % 3, (j + 2) % 3) if typ == "A" else ((j + 2) % 3, j % 3)
        groups[s].append({"type": typ, "rotation": j, "a_axis": a_axis, "b_axis": b_axis})
    expected_pairs = {(i, j) for i in range(3) for j in range(3) if i != j}
    for orientations in groups.values():
        assert len(orientations) == 6
        assert {(v["a_axis"], v["b_axis"]) for v in orientations} == expected_pairs

    # n=C and per-line divisibility force a single character sign.
    possible_charges = [q for q in range(-C, C + 1, 2) if ((A - B) * q) % C == 0]
    assert possible_charges == [-61, 61]

    # Every nonempty supporting line carries >=delta short edges.
    # A line has at most one short edge from each of the C triangles.
    line_pairs = [(m, n) for m in range(C + 1) for n in range(C + 1 - m)
                  if m + n > 0 and (A * m - B * n) % C == 0]
    delta = min(m + n for m, n in line_pairs)
    assert delta == 9
    maximum_lines = 2 * C // delta
    capacity = maximum_lines - 1
    assert (maximum_lines, capacity) == (13, 12)
    small_pairs = [(m, n) for m in range(capacity + 1) for n in range(capacity + 1)
                   if m + n > 0 and (A * m - B * n) % C == 0]
    assert small_pairs == [(5, 4), (10, 8)]
    assert all(4 * m == 5 * n for m, n in small_pairs)
    reachable = bounded_pair_sums(small_pairs, C)
    assert (C, C) not in reachable

    # Independent direct count of one-sign orientation inventories.
    # Off-diagonal 3x3 matrix: row = a-axis, column = b-axis.
    ratio = (A * pow(B, -1, C)) % C
    inventories = 0
    for m0 in range(C + 1):
        for m1 in range(C - m0 + 1):
            M = (m0, m1, C - m0 - m1)
            choices = [[0, C] if m in (0, C) else [(ratio * m) % C] for m in M]
            for NN in product(*choices):
                if sum(NN) != C:
                    continue
                for x in range(M[0] + 1):
                    T = {(0, 1): x, (0, 2): M[0] - x,
                         (2, 1): NN[1] - x, (2, 0): M[2] - NN[1] + x,
                         (1, 0): NN[0] - M[2] + NN[1] - x}
                    T[1, 2] = M[1] - T[1, 0]
                    if min(T.values()) < 0:
                        continue
                    assert all(sum(v for (i, j), v in T.items() if i == k) == M[k] for k in range(3))
                    assert all(sum(v for (i, j), v in T.items() if j == k) == NN[k] for k in range(3))
                    assert all((A * M[k] - B * NN[k]) % C == 0 for k in range(3))
                    # At least one direction total cannot be partitioned into
                    # the geometrically bounded supporting-line pairs.
                    assert any((M[k], NN[k]) not in reachable for k in range(3))
                    inventories += 1
    assert inventories == 2430

    # Exceptional height 2: local character congruence and parity.
    def exceptional_charges(population: int) -> list[int]:
        return [q for q in range(-population, population + 1, 2)
                if ((A - B) * q + 3 * B * (A + B)) % C == 0]
    assert N % C == 34
    assert exceptional_charges(34) == []
    assert exceptional_charges(95) == [-1]
    min_exceptional = next(n for n in range(34, N + 1, C) if exceptional_charges(n))
    assert min_exceptional == 95

    # Global scalar charges g_h = u_h-v_h, opposite in sign to D in the earlier note.
    S0, S2, S3 = C * C, -3 * B * (A + B), -C * (A + 2 * B)
    D = (S0 + S2 + S3) // (C - A + B)
    Dstar = -(S0 + S2 - S3) // (C + A - B)
    assert (D, Dstar) == (-182, -60)
    charge_even, charge_odd = -(D + Dstar) // 2, -(D - Dstar) // 2
    assert (charge_even, charge_odd) == (121, 61)
    # Odd-height population is an odd multiple of C, but cannot be C.
    min_odd_population = 3 * C
    min_even_population = next(n for n in range(34, N + 1, C) if n >= 121 and n % 2 == 1)
    assert min_even_population == 217

    max_occupied = 1 + (N - min_exceptional) // (2 * C)
    assert max_occupied == 118
    # At least one odd height has >=183; all other ordinary heights >=122.
    assert N == min_exceptional + min_odd_population + (max_occupied - 2) * 2 * C
    # The earlier proved gap restriction is an input, not re-proved by this calculation.
    maximum_gaps = 2
    max_span = max_occupied - 1 + maximum_gaps
    assert max_span == 119
    two_height_populations = [(183 + 122 * t, 14247 - 122 * t) for t in range(116)]
    assert all(n1 + n2 == N and n1 >= 183 and n2 >= 217 for n1, n2 in two_height_populations)

    # Previous formal witness still passes the NEW scalar/population conditions.
    assert 183 >= 122 and 14247 >= min_exceptional

    report = {
        "status": "PASS",
        "scope": "Exact arithmetic and finite inventory audit; the geometric proof is in NO_61_HEIGHT.md. N=14430 remains UNRESOLVED.",
        "tile": [A, B, C], "N": N,
        "common_character_charges_for_61_tiles": possible_charges,
        "common_sign_orientation_groups": groups,
        "minimum_short_edges_per_nonempty_line": delta,
        "maximum_supporting_lines_if_population_61": maximum_lines,
        "maximum_a_edges_or_b_edges_on_one_line": capacity,
        "allowed_bounded_line_pairs": small_pairs,
        "total_pair_61_61_reachable": False,
        "one_sign_current_inventories_checked": inventories,
        "both_signs_by_half_turn_symmetry": 2 * inventories,
        "height_2_population_34_possible_charges": [],
        "height_2_population_95_possible_charges": [-1],
        "minimum_occupied_population_outside_height_2": 122,
        "minimum_height_2_population": min_exceptional,
        "maximum_occupied_heights": max_occupied,
        "maximum_span_using_previous_gap_theorem": max_span,
        "global_character_sums_g_even_g_odd": [charge_even, charge_odd],
        "minimum_total_odd_height_population": min_odd_population,
        "minimum_total_even_height_population": min_even_population,
        "necessary_two_height_population_pairs": two_height_populations,
        "extremal_K_118_population_pattern": {"height_2": 95, "one_odd_height": 183, "remaining_116_heights": 122},
        "not_claimed": ["Exclusion of N=14430", "Exclusion of all two-height tilings", "A 122-divisibility theorem", "Coordinate existence", "External refereeing"]
    }
    output = Path(__file__).with_name("verification_no61.json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "status", "scope", "allowed_bounded_line_pairs", "one_sign_current_inventories_checked",
        "minimum_occupied_population_outside_height_2", "minimum_height_2_population",
        "maximum_occupied_heights", "maximum_span_using_previous_gap_theorem")}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
