#!/usr/bin/env python3
"""Exact replay of the two-odd-height five-block exclusion at 5063."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "research").is_dir() and (p / "scripts").is_dir())
PACKAGE = ROOT / "research/2026-11-21/semiprimes"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def arithmetic_controls():
    a, b, c, d = 35, 13, 43, 22
    assert a*a+a*b+b*b == c*c
    pure_cap = (8*2*c)//43
    assert pure_cap == 16
    monochromatic = []
    for sigma in (1, -1):
        possible_o = (0, 1-2*sigma)
        permitted_Q = [sigma*m for m in range(1, pure_cap+1)]
        compatible = [(o, Q) for o in possible_o for Q in permitted_Q if (Q+c*o) % d == 0]
        assert not compatible
        monochromatic.append({"sign": sigma, "other_layer_odd_charge_blocks": 1-2*sigma,
                              "remote_subtree_charge_blocks": list(possible_o),
                              "permitted_nonzero_remote_currents": compatible})
    assert 2*pure_cap < 2*c
    # The balanced 2c layer and charged 3c layer cannot split across an upper cut.
    assert all((c*t) % d for t in (1, 2))
    # Reflecting normalized coordinates by -conjugation preserves sign and swaps hand.
    for j, hand in itertools.product(range(6), (-1, 1)):
        old = hand*((-1)**j)
        new = -hand*((-1)**((3-j) % 6))
        assert old == new
    total_exterior_character = -3*a*b
    assert d*d-total_exterior_character == c*c
    for e in range(-10, 11):
        numerator = d*(d+c*e)-total_exterior_character
        assert numerator == c*(c+d*e)
    assert (8*(2*c)+35*c)//43 == 51
    return {"monochromatic_middle_capacity": pure_cap,
            "remote_gate_residue_checks": monochromatic,
            "monochromatic_native_gate_total_capacity": 2*pure_cap,
            "monochromatic_middle_population": 2*c,
            "balanced_middle_median_parameters": [1, 2],
            "median_K_never_zero_for_these_parameters": True,
            "reflection_preserves_sign_and_exchanges_hands": True,
            "whole_exterior_character": total_exterior_character,
            "even_core_signed_residue": d,
            "single_special_current_offset": c}


def universe_counts():
    c, d, cap, ordinary = 43, 22, 51, 85
    rows = []
    visited = reserved = 0
    for p in range(4):
        for m in range(2):
            u = m-p
            q = c+d*u
            if not (-c <= q <= cap):
                continue
            patterns = sum(math.comb(ordinary, k)*math.comb(k, p-k)*(ordinary-k)**m
                           for k in range(p+1) if k <= p <= 2*k)
            visited += patterns
            passes = max(q, 0)+d*p <= 2*c and max(-q, 0)+d*m <= c
            if passes:
                reserved += patterns
            rows.append({"positive_units": p, "negative_units": m,
                         "special_integer_charge": u, "special_current": q,
                         "profiles": patterns, "all_pass_sign_reserves": passes})
    assert visited == reserved == 9112001
    return {"ordinary_bins": ordinary, "visited": visited, "reserve_passed": reserved,
            "derivation_by_block_counts": rows}


def brute_small(c, d, cap, cuts):
    """Cartesian signed vectors; does not use the C++ multiset recursion."""
    accepted = set()
    visited = reserved = 0
    for remote in itertools.product(range(-1, cap//d+1), repeat=2*c-1):
        positive = sum(max(g, 0) for g in remote)
        negative = sum(max(-g, 0) for g in remote)
        if positive > 2*c//d or negative > c//d:
            continue
        u = -sum(remote)
        q = c+d*u
        if not (-c <= q <= cap):
            continue
        visited += 1
        if max(q, 0)+d*positive > 2*c or max(-q, 0)+d*negative > c:
            continue
        reserved += 1
        up = [q] + [d*g for g in remote[:c-1]]
        down = [d*g for g in remote[c-1:]]
        assert len(up) == len(down) == c
        valid = True
        for D, wu, wd in cuts:
            # Test all ordered pairs of shifts directly, independently of max+max.
            for su, sd in itertools.product(range(c), repeat=2):
                value = sum(up[r]*wu[(r+su) % c]+down[r]*wd[(r+sd) % c] for r in range(c))
                if value > 3*c*D:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            accepted.add((u, remote))
    return accepted, visited, reserved


def small_controls(binary):
    cases = [(3, 2, 4, []), (4, 3, 5, []),
             (5, 3, 5, [(2, [3, -2, 1, 0, -3], [-1, 3, -2, 2, 0]),
                        (1, [-2, 0, 3, 1, -1], [2, -3, 0, 1, 2])])]
    reports = []
    for c, d, cap, cuts in cases:
        expected, visited, reserved = brute_small(c, d, cap, cuts)
        lines = [f"{c} {d} {cap} {2*c//d} {c//d} {len(cuts)} 100000000"]
        for D, up, down in cuts:
            lines += [str(D), " ".join(map(str, up)), " ".join(map(str, down))]
        proc = subprocess.run([str(binary)], input="\n".join(lines)+"\n",
                              text=True, capture_output=True, check=True)
        records = [json.loads(line) for line in proc.stdout.splitlines()]
        summary = records.pop()
        actual = set()
        for record in records:
            remote = [0]*(2*c-1)
            for i in record["positive_indices"]:
                remote[i] += 1
            if record["negative_index"] >= 0:
                remote[record["negative_index"]] -= 1
            item = (record["special_up_charge"], tuple(remote))
            assert item not in actual
            actual.add(item)
        assert summary["exhaustive"] is True
        assert actual == expected
        assert summary["visited"] == visited
        assert summary["reserve_passed"] == reserved
        assert summary["cut_passed"] == len(expected)
        reports.append({"c": c, "d": d, "capacity": cap, "cuts": len(cuts),
                        "visited": visited, "reserve_passed": reserved,
                        "survivors": len(expected), "status": "PASS"})
    return reports


def check_certificate_columns():
    index = json.loads((PACKAGE / "gate-model/CERTIFICATES_5063.json").read_text())
    spec = importlib.util.spec_from_file_location("existing_independent_profile_audit",
                                                PACKAGE / "audit/verify_profile_duals.py")
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    reports, cuts = [], []
    for entry in index["certificates"]:
        path = ROOT / entry["path"]
        assert sha(path) == entry["sha256"]
        report, variants = audit.verify(path)
        assert tuple(report["tile"]) == (35, 13, 43)
        reports.append(report)
        cuts.extend(variants)
    assert len(reports) == 65 and sum(x["columns"] for x in reports) == 1442220
    cut_path = ROOT / index["cut_file"]
    assert sha(cut_path) == index["cut_file_sha256"]
    transformed = audit.check_cut_file(cut_path, cuts, (35, 13, 43))
    symmetries = audit.verify_geometry_symmetries(35, 13, 43)
    return reports, transformed, symmetries, cut_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saved-enumeration", action="store_true")
    parser.add_argument("--out", type=Path, default=HERE / "SINGLE_OFFSET_REPLAY.json")
    args = parser.parse_args()
    start = time.monotonic()
    arithmetic = arithmetic_controls()
    universe = universe_counts()
    certificates, transforms, symmetries, cut_path = check_certificate_columns()
    print("EXACT_65_CERTIFICATES_AND_780_TRANSFORMS=PASS", flush=True)
    source = HERE / "enumerate_single_offset.cpp"
    enumeration_path = HERE / "FULL_SINGLE_OFFSET_ENUMERATION_5063.json"
    with tempfile.TemporaryDirectory(prefix="ep634-single-offset-") as td:
        binary = Path(td)/"enumerate_single_offset"
        subprocess.run(["g++", "-O3", "-std=c++17", str(source), "-o", str(binary)],
                       text=True, capture_output=True, check=True)
        controls = small_controls(binary)
        print("INDEPENDENT_CARTESIAN_ENUMERATION_CONTROLS=PASS", flush=True)
        if args.saved_enumeration:
            result = json.loads(enumeration_path.read_text())
        else:
            proc = subprocess.run([str(binary), "0"], input=cut_path.read_text(),
                                  text=True, capture_output=True, check=True, timeout=900)
            rows = [json.loads(line) for line in proc.stdout.splitlines()]
            assert len(rows) == 1, "A surviving profile was emitted."
            result = rows[0]
            write_json(enumeration_path, result)
    assert result["summary"] is True and result["exhaustive"] is True
    assert result["visited"] == universe["visited"] == 9112001
    assert result["reserve_passed"] == universe["reserve_passed"] == 9112001
    assert result["cut_passed"] == 0
    assert len(result["rejected"]) == 780
    assert sum(result["rejected"]) == 9112001
    report = {
        "status": "PASS", "tile": [35, 13, 43],
        "scope": "Exact necessary single-offset profile exclusion, with written geometric reduction. Both two-odd-height 215 modes are excluded; neither full tile count is decided.",
        "excluded_five_block_height_populations": [{"1": 86, "-1": 129}, {"1": 86, "3": 129}],
        "remaining_five_block_odd_height_population": {"1": 215},
        "remaining_five_block_short_heights": [0, 1, 2],
        "full_5063_excluded": False, "full_3431_excluded": False,
        "fresh_exhaustive_enumeration": not args.saved_enumeration,
        "arithmetic_controls": arithmetic,
        "profile_universe": universe,
        "base_certificates": len(certificates),
        "column_inequalities": sum(x["columns"] for x in certificates),
        "certificates": certificates,
        "serialized_cuts": transforms,
        "geometric_symmetries": symmetries,
        "small_independent_controls": controls,
        "complete_enumeration": result,
        "enumerator_sha256": sha(source),
        "cut_file_sha256": sha(cut_path),
        "enumeration_sha256": sha(enumeration_path),
        "seconds": time.monotonic()-start,
    }
    write_json(args.out, report)
    print(json.dumps({key: report[key] for key in (
        "status", "fresh_exhaustive_enumeration", "base_certificates", "column_inequalities",
        "remaining_five_block_short_heights", "full_5063_excluded", "full_3431_excluded", "seconds")}, indent=2))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    main()
