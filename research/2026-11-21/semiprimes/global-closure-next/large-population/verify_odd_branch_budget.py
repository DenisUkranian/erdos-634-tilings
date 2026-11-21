#!/usr/bin/env python3
"""Exact finite controls for GLOBAL_ODD_BRANCH_BUDGET.md.

No optimizer is imported. Geometric completeness is proved in the note;
this program checks its finite arithmetic and the identity/accounting of
its already independently verified 65-certificate dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "research").is_dir() and (p / "scripts").is_dir())
PACKAGE = ROOT / "research/2026-11-21/semiprimes"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def one_sign_search(c: int, d: int, cap: int, sigma: int, max_blocks: int = 11):
    """Independent sign-block allocations, not an assumed minimizer formula.

The child/complement populations are unions of ordinary odd exact nodes.
A total of one block is impossible for either union. Enumerating every
allocation of their two signs includes cases which geometry may exclude;
only infeasibility below the stated threshold is used in the proof.
"""
    rows = []
    first = None
    for K in range(1, max_blocks + 1, 2):
        p_total, m_total = (K + 1) // 2, (K - 1) // 2
        p_rest = p_total - (2 if sigma > 0 else 0)
        m_rest = m_total - (2 if sigma < 0 else 0)
        feasible = []
        if min(p_rest, m_rest) >= 0:
            for p in range(p_rest + 1):
                for m in range(m_rest + 1):
                    if p + m == 1 or (p_rest - p) + (m_rest - m) == 1:
                        continue
                    o = p - m
                    for magnitude in range(1, cap + 1):
                        Q = sigma * magnitude
                        numerator = Q + c * o
                        if numerator % d:
                            continue
                        e = numerator // d
                        assert Q == d * e - c * o
                        feasible.append({
                            "child_odd_sign_blocks": [p, m],
                            "complement_odd_sign_blocks": [p_rest - p, m_rest - m],
                            "odd_charge_blocks": o,
                            "even_charge_blocks": e,
                            "Q": Q,
                        })
        if feasible and first is None:
            first = K
        rows.append({"odd_blocks": K, "arithmetically_feasible_allocations": len(feasible),
                     "first_allocation": feasible[0] if feasible else None})
    return {"sign": sigma, "first_arithmetic_block_count": first, "rows": rows}


def charge_cost(k: int) -> int:
    return 3 if abs(k) == 1 else abs(k)


def check_four_block_equality():
    # Every nonzero charge costs >=2 blocks, so at most two can appear.
    solutions = []
    for length in (1, 2):
        for charges in itertools.product([i for i in range(-4, 5) if i], repeat=length):
            if sum(charges) or sum(map(charge_cost, charges)) > 4:
                continue
            solutions.append(list(charges))
    assert solutions == [[-2, 2], [2, -2]]
    return {"nonzero_zero_sum_charge_lists_cost_at_most_four": solutions,
            "minimum_extra_odd_blocks": 4,
            "seven_total_blocks_force_negative_monochromatic_two_block_node": True}


def profile_counts():
    c, d, cap = 43, 22, 51
    n = 2 * (c - 1)
    visited = reserve_passed = 0
    native_up = set()
    for p in range(4):
        for m in range(2):
            for k in range(p + 1):
                if not (k <= p <= 2*k):
                    continue
                remote = comb(n, k) * comb(k, p-k) * (n-k)**m
                for u in range(-2*c, 2*c + 1):
                    q0 = 2*c + d*u
                    if not (-c <= q0 <= cap):
                        continue
                    native_up.add(u)
                    v = -u - p + m
                    q1 = -c + d*v
                    if not (-c <= q1 <= cap):
                        continue
                    visited += remote
                    if max(q0, 0) + max(q1, 0) + d*p > 2*c:
                        continue
                    if max(-q0, 0) + max(-q1, 0) + d*m > c:
                        continue
                    reserve_passed += remote
    assert native_up == {-5, -4, -3, -2}
    assert (visited, reserve_passed) == (34672599, 17800359)
    return {"visited": visited, "reserve_passed": reserve_passed,
            "native_up_integer_parameters": sorted(native_up),
            "remote_integer_parameters": [i for i in range(-5, 6) if -c <= d*i <= cap],
            "remote_positive_unit_budget": 2*c//d,
            "remote_negative_unit_budget": c//d}


def check_cut_offsets():
    a, b, c, d = 35, 13, 43, 22
    A, B = b*(2*a+b), a*(a+2*b)
    assert a*a + a*b + b*b == c*c
    assert A+B == 2*c*c - d*d
    checked = 0
    for e, o in itertools.product(range(-5, 6), repeat=2):
        for native in (False, True):
            G_even = c*e + (d if native else 0)
            G_odd = c*o
            exterior = -(A+B) if native else 0
            Q = Fraction(d*G_even - c*G_odd - exterior, c)
            assert Q == (2*c if native else 0) + d*e-c*o
            G_even = c*e
            exterior = c*c if native else 0
            Q = Fraction(d*G_even - c*G_odd - exterior, c)
            assert Q == (-c if native else 0) + d*e-c*o
            checked += 2
    gate_pairs = {( (a*y-b*x) % c, (a*x-b*y) % c)
                  for x, y in itertools.product(range(c), repeat=2)}
    assert len(gate_pairs) == c*c
    return {"exterior_base_character": c*c,
            "exterior_height_two_character": -(A+B),
            "upward_native_current_offset": 2*c,
            "downward_native_current_offset": -c,
            "integer_substitution_controls": checked,
            "independent_gate_shift_pairs": len(gate_pairs),
            "proof": "The displayed polynomial identities, not a finite-height inference."}


def check_median_localization():
    possible = []
    for middle_below, extra_below in itertools.product((False, True), repeat=2):
        # The middle layer has charge +c; the other layer is balanced.
        t = int(middle_below) + 1
        assert t in (1, 2)
        # K=(c-d)t-d*j0 can vanish only when d divides t.
        assert (43*t) % 22 != 0
        # A real nonzero K supplies a height-one bank tile below the path.
        if not middle_below:
            continue
        assert t == 2
        possible.append({"middle_below": True, "extra_below": extra_below, "t": t})
    return {"remaining_whole_layer_side_allocations": possible,
            "path_step_vectors_after_division_by_z": [[43, 0], [35, 13]],
            "native_anchor_from_actual_height_two_step": True}


def check_prior_certificate_identity():
    index_path = PACKAGE / "gate-model/CERTIFICATES_5063.json"
    audit_path = PACKAGE / "audit/FINAL_DUAL_REPLAY_5063.json"
    enumeration_path = PACKAGE / "gate-model/FINAL_PROFILE_ENUMERATION_5063.jsonl"
    index = json.loads(index_path.read_text())
    audit = json.loads(audit_path.read_text())
    enumeration = json.loads(enumeration_path.read_text())
    assert index["tile"] == [35, 13, 43]
    assert index["base_certificates"] == len(index["certificates"]) == 65
    assert index["transformed_cuts"] == 780
    audit_by_hash = {row["sha256"]: row for row in audit["certificates"]}
    assert len(audit_by_hash) == 65
    columns = 0
    for row in index["certificates"]:
        assert digest(ROOT / row["path"]) == row["sha256"]
        checked = audit_by_hash[row["sha256"]]
        assert checked["status"] == "PASS"
        assert checked["columns"] == 12*43*43
        assert checked["maximum_score"] <= checked["D"]
        columns += checked["columns"]
    assert columns == index["total_column_inequalities"] == 1442220
    assert digest(ROOT / index["cut_file"]) == index["cut_file_sha256"]
    assert digest(ROOT / index["enumerator_source"]) == index["enumerator_source_sha256"]
    assert enumeration["exhaustive"] is True
    assert enumeration["visited"] == index["complete_profile_count"] == 34672599
    assert enumeration["reserve_passed"] == index["after_sign_reserves"] == 17800359
    assert enumeration["cut_passed"] == index["surviving_profiles"] == 0
    assert sum(enumeration["rejected"]) == enumeration["reserve_passed"]
    assert len(enumeration["rejected"]) == 780
    return {"certificate_files_hashed": 65, "saved_column_checks": columns,
            "saved_transformed_cuts": 780, "saved_exhaustive_profiles": enumeration["visited"],
            "saved_sign_reserve_profiles": enumeration["reserve_passed"],
            "saved_survivors": 0,
            "replayed_here": "Hashes and saved accounting only; full prior integer replay remains an explicit proof dependency.",
            "index_sha256": digest(index_path), "independent_audit_sha256": digest(audit_path),
            "enumeration_sha256": digest(enumeration_path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "ODD_BRANCH_BUDGET_REPLAY.json")
    args = parser.parse_args()
    cap43 = (8*2*43)//43
    cap37 = (43*2*37)//222
    assert cap43 == 16 and cap37 == 14
    pos = one_sign_search(43, 22, cap43, 1)
    neg = one_sign_search(43, 22, cap43, -1)
    assert pos["first_arithmetic_block_count"] == 7
    assert neg["first_arithmetic_block_count"] == 9
    control37 = [one_sign_search(37, 26, cap37, s, max_blocks=5) for s in (1, -1)]
    assert all(r["first_arithmetic_block_count"] == 5 for r in control37)
    control7 = [one_sign_search(7, 2, 7, s, max_blocks=5) for s in (1, -1)]
    assert all(r["first_arithmetic_block_count"] == 5 for r in control7)
    result = {
        "status": "PASS",
        "tile": [35, 13, 43],
        "native_middle_hypotheses": {"population": 129, "positive": 86, "negative": 43, "class": "zR"},
        "monochromatic_two_block_parent_gate_capacity": cap43,
        "positive_remote_node_global_odd_minimum": 301,
        "negative_remote_node_global_odd_minimum": 387,
        "arithmetic_allocation_checks": [pos, neg],
        "3431_nontransfer_controls": control37,
        "143_no_universal_7_or_9_block_inference": control7,
        "four_block_equality": check_four_block_equality(),
        "native_cut_offsets": check_cut_offsets(),
        "unchanged_profile_universe": profile_counts(),
        "median_localization": check_median_localization(),
        "prior_exact_certificate_dependency": check_prior_certificate_identity(),
        "conditional_native_middle_global_odd_minimum": 387,
        "five_block_n1_equal_129_excluded": True,
        "five_block_remaining_height_populations": [
            {"odd_heights": [1], "populations": {"1": 215}},
            {"odd_heights": [-1, 1], "populations": {"-1": 129, "1": 86}},
            {"odd_heights": [1, 3], "populations": {"1": 86, "3": 129}},
        ],
        "full_5063_excluded": False,
        "full_3431_excluded": False,
        "scope": "Exact finite controls of the written geometric theorem and identity of its prior certificate dependency. No finite height enumeration or numerical optimization is used as an unrestricted proof.",
    }
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "output": str(args.out),
                      "positive_remote_2c_minimum": 301, "negative_remote_2c_minimum": 387,
                      "native_middle_conditional_minimum": 387,
                      "full_5063_excluded": False, "full_3431_excluded": False}))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    main()
