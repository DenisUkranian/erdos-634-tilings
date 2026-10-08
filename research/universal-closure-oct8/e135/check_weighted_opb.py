#!/usr/bin/env python3
"""Independently check the native OPB file against the audited DSU model/map."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def equation(line, n):
    tokens = line.split()
    require(len(tokens) >= 3 and tokens[-1] == ";" and tokens[-3] == "=",
            "Malformed OPB equality")
    rhs = int(tokens[-2])
    terms = tokens[:-3]
    require(len(terms) % 2 == 0, "Malformed OPB terms")
    coefficients = {}
    for c, x in zip(terms[::2], terms[1::2]):
        require(re.fullmatch(r"[+-][0-9]+", c) is not None, "Bad coefficient")
        require(re.fullmatch(r"x[1-9][0-9]*", x) is not None, "Bad variable")
        c, x = int(c), int(x[1:])
        require(1 <= x <= n and x not in coefficients and c != 0,
                "Repeated/zero/out-of-range coefficient")
        coefficients[x] = c
    return rhs, coefficients


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("prefix")
    p.add_argument("opb", type=Path)
    p.add_argument("report", type=Path)
    p.add_argument("--count", type=int, default=135)
    a = p.parse_args()
    model = Path(a.prefix + ".model.txt")
    mapping = Path(a.prefix + ".map.txt")
    with model.open() as f, a.opb.open() as opb:
        n, selected = map(int, next(f).split())
        require(selected == 0, "Unexpected selected metadata")
        metadata = [tuple(map(int, next(f).split())) for _ in range(n)]
        require({m[0] for m in metadata} == set(range(n)), "Nonbijective new variable indices")
        representatives = {m[1]: m[0] + 1 for m in metadata}
        require(len(representatives) == n, "Repeated representatives")
        match = re.fullmatch(r"\* #variable= (\d+) #constraint= (\d+) #equal= (\d+) intsize= 32\n?",
                             next(opb))
        require(match is not None, "Wrong OPB header")
        number_variables, number_rows, number_equalities = map(int, match.groups())
        require(number_variables == n and number_rows == number_equalities, "Header counts")
        checked_rows = 0
        max_row_size = 0
        for line in f:
            rhs, size, *literals = map(int, line.split())
            require(size == len(literals), "Source row size")
            coefficients = Counter()
            for lit in literals:
                require(1 <= abs(lit) <= n, "Source literal range")
                coefficients[abs(lit)] += 1 if lit > 0 else -1
            coefficients = {x: c for x, c in coefficients.items() if c}
            require(equation(next(opb), n) == (rhs, coefficients), "OPB current row mismatch")
            max_row_size = max(max_row_size, abs(rhs), sum(abs(c) for c in coefficients.values()))
            checked_rows += 1
        constant = 0
        weights = Counter()
        fixed_counts = Counter()
        with mapping.open() as mp:
            original_n = int(next(mp))
            seen = 0
            for seen, line in enumerate(mp, 1):
                original, root, flip, value = map(int, line.split())
                require(original == seen and 1 <= root <= original_n and
                        flip in (0, 1) and value in (-1, 0, 1), "Bad DSU map")
                fixed_counts[value] += 1
                if value >= 0:
                    constant += value
                else:
                    require(root in representatives, "Missing representative")
                    weights[representatives[root]] += (-1 if flip else 1)
                    constant += flip
            require(seen == original_n, "Incomplete map")
        weights = {x: c for x, c in weights.items() if c}
        require(equation(next(opb), n) == (a.count - constant, weights),
                "Weighted original-tile count does not match affine expansion")
        require(not any(line.strip() for line in opb), "Trailing OPB constraints")
        require(checked_rows + 1 == number_rows, "OPB row count")
        max_row_size = max(max_row_size, abs(a.count - constant), sum(abs(c) for c in weights.values()))
        require(max_row_size < 2**31, "Declared intsize insufficient for input rows")
    result = {
        "status": "PASS", "variables": n, "current_equalities": checked_rows,
        "total_equalities": number_rows, "original_tile_count": a.count,
        "original_variables": original_n, "original_variable_fixed_counts": dict(fixed_counts),
        "count_constant": constant, "nonzero_count_weights": len(weights),
        "count_weight_range": [min(weights.values()), max(weights.values())],
        "all_repeated_literal_multiplicities_preserved": True,
        "all_opb_equalities_literally_compared": True,
        "original_tile_count_reconstructed_from_affine_dsu_map": True,
        "largest_input_row_l1_bound": max_row_size,
        "sha256": {str(x): hashlib.sha256(x.read_bytes()).hexdigest()
                   for x in (model, mapping, a.opb)},
        "unsatisfiability_checked": False,
    }
    a.report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
