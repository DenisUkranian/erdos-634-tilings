#!/usr/bin/env python3
"""Independently check the exact E135 universal placement/current model.

This checker uses endpoint points and primitive directions as row keys, then
compares literal equations as a multiset. It does not call either placement
generator, its row sorter, the propagator, or a solver. No UNSAT claim is made.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import struct
import time

if not __debug__:
    raise RuntimeError("Run this exact verifier without Python -O or -OO.")

POOL_SHA = "7a9182ff37328cc6e5b7c6fe822bbcf529687ecd12a0bc31927e6633d71f715a"
PACK = struct.Struct("<6q")


def check(test, message):
    if not test:
        raise ValueError(message)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def norm(a):
    return a[0] * a[0] + a[0] * a[1] + a[1] * a[1]


def multiply(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0] + a[1] * b[1])


def power(a, n):
    out = (1, 0)
    for _ in range(n):
        out = multiply(out, a)
    return out


def file_sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("geometry", type=Path)
    ap.add_argument("model", type=Path)
    ap.add_argument("report", type=Path)
    ap.add_argument("--reference-prefix", type=Path,
                    help="Audited seven-level pool; default strips .geometry.txt")
    args = ap.parse_args()
    started = time.monotonic()
    rows = defaultdict(list)
    boundary = Counter()
    heights = []
    triangles = []
    factor = 7**5
    unit_square = 7**6

    def events(vertices):
        for k in range(3):
            p, q = vertices[k], vertices[(k + 1) % 3]
            dx, dy = sub(q, p)
            divisor = math.gcd(dx, dy)
            check(divisor > 0, "Zero edge")
            dx, dy = dx // divisor, dy // divisor
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            # Point plus direction uniquely specifies the line and endpoint.
            yield (dx, dy, p[0], p[1]), 1
            yield (dx, dy, q[0], q[1]), -1

    with args.geometry.open() as f:
        marker, np, nt = map(int, next(f).split())
        check((marker, nt) == (1, 246600), "Unexpected geometry header")
        points = [tuple(map(int, next(f).split())) for _ in range(np)]
        check(all(len(p) == 2 for p in points), "Bad coordinate")
        check(len(set(points)) == np, "Repeated point")
        target = points[:3]
        check(target == [(0, 0), (45 * 343, 0), (0, 45 * 343)],
              "Unexpected target or coordinate scale")
        target_area = cross(sub(target[1], target[0]), sub(target[2], target[0]))
        check(target_area == 135 * 15 * unit_square, "Area ratio")
        for j in range(nt):
            values = list(map(int, next(f).split()))
            check(len(values) == 5, "Bad triangle record")
            indices, height = values[:3], values[3]
            check(len(set(indices)) == 3 and all(0 <= k < np for k in indices),
                  "Bad vertex index")
            vs = [points[k] for k in indices]
            check(sorted(norm(sub(vs[k], vs[(k + 1) % 3])) for k in range(3))
                  == [9 * unit_square, 25 * unit_square, 49 * unit_square],
                  "Triangle is not a (3,5,7) congruent tile")
            check(cross(sub(vs[1], vs[0]), sub(vs[2], vs[0])) == 15 * unit_square,
                  "Wrong signed tile area")
            check(all(cross(sub(target[(k + 1) % 3], target[k]), sub(p, target[k])) >= 0
                      for p in vs for k in range(3)), "Tile leaves the target")
            heights.append(height)
            triangles.append(tuple(z * factor for p in sorted(vs) for z in p))
            for key, sign in events(vs):
                rows[key].append(sign * (j + 1))
        check(not any(line.strip() for line in f), "Trailing geometry records")
    check(len(set(triangles)) == nt, "Repeated tile placement")
    reference = args.reference_prefix
    if reference is None:
        check(str(args.geometry).endswith(".geometry.txt"), "Supply reference prefix")
        reference = Path(str(args.geometry)[:-len(".geometry.txt")])
    reference_report = json.loads(Path(str(reference) + ".json").read_text())
    check((reference_report["L"], reference_report["U"],
           reference_report["basis_rotation"]) == (-3, 3, 0), "Reference coordinate frame")
    check(not reference_report["incomplete"] and not reference_report["conflict"],
          "Reference reduction did not complete")
    templates = []
    for height in range(-3, 4):
        short_unit = multiply(power((2, 1), height + 3), power((3, -1), 3 - height))
        for first_length, second_length in [(3, 5), (5, 3)]:
            for rotation in range(6):
                u = multiply(short_unit, power((0, 1), rotation))
                v = multiply(u, (-1, 1))
                templates.append(((0, 0),
                                  (first_length * u[0], first_length * u[1]),
                                  (second_length * v[0], second_length * v[1])))
    expected_triangles = set()
    with Path(str(reference) + ".remaining.txt").open() as f:
        check(tuple(map(int, next(f).split())) == (-3, 3, nt), "Reference pool header")
        for line in f:
            orientation, x, y = map(int, line.split())
            check(0 <= orientation < len(templates), "Reference template index")
            vs = sorted((x + dx, y + dy) for dx, dy in templates[orientation])
            record = tuple(z * factor for p in vs for z in p)
            item = record, orientation // 12 - 3
            check(item not in expected_triangles, "Reference has repeated placement")
            expected_triangles.add(item)
    check(set(zip(triangles, heights)) == expected_triangles,
          "Literal physical reference pool and geometry differ")
    del expected_triangles
    digest = hashlib.sha256()
    for triangle in sorted(triangles):
        digest.update(PACK.pack(*triangle))
    pool_sha = digest.hexdigest()
    check(pool_sha == POOL_SHA, "Physical pool differs from audited universal pool")
    del triangles

    for key, sign in events(target):
        boundary[key] += sign
    expected = Counter()
    entries = 0
    for key in set(rows) | set(boundary):
        terms = rows.get(key, [])
        check(len({abs(lit) for lit in terms}) == len(terms),
              "Same tile contributes twice to one geometric endpoint")
        if terms:
            expected[(boundary[key], tuple(sorted(terms)))] += 1
            entries += len(terms)
        else:
            check(boundary[key] == 0, "Unmatched target endpoint")
    expected_row_count = sum(expected.values())
    del rows, boundary

    model_rows = 0
    model_entries = 0
    with args.model.open() as f:
        nv, selected = map(int, next(f).split())
        check((nv, selected) == (nt, 0), "Model does not preserve every pool variable")
        for j in range(nv):
            check(tuple(map(int, next(f).split())) == (j, j, 0, heights[j]),
                  "Model variable metadata is not the geometry bijection")
        for line in f:
            if not line.strip():
                continue
            values = tuple(map(int, line.split()))
            rhs, count, *terms = values
            check(count == len(terms) and count > 0, "Bad model row size")
            check(all(1 <= abs(lit) <= nv for lit in terms), "Bad model variable")
            check(len({abs(lit) for lit in terms}) == len(terms), "Repeated model variable")
            signature = rhs, tuple(sorted(terms))
            check(expected[signature] > 0, "Extra or incorrect endpoint equation")
            expected[signature] -= 1
            if expected[signature] == 0:
                del expected[signature]
            model_rows += 1
            model_entries += len(terms)
    check(not expected, "Missing endpoint equations")
    check((model_rows, model_entries) == (expected_row_count, entries), "Equation totals")
    report = {
        "status": "PASS",
        "geometry_sha256": file_sha(args.geometry),
        "model_sha256": file_sha(args.model),
        "physical_pool_sha256_at_denominator_7_to_8": pool_sha,
        "placements": nt,
        "coordinate_frame_physical_denominator": 343,
        "target_physical_sides": [45, 45, 45],
        "tile_physical_sides": [3, 5, 7],
        "signed_area_ratio": 135,
        "height_populations": dict(sorted(Counter(heights).items())),
        "current_equations": model_rows,
        "signed_nonzero_entries": model_entries,
        "all_tiles_exact_metric_contained_unique_and_ccw": True,
        "every_pool_variable_present_once": True,
        "reference_pool_compared_as_literal_exact_physical_set": True,
        "independent_equations_compared_as_literal_multiset": True,
        "all_arithmetic_exact": True,
        "unsatisfiability_checked": False,
        "wall_seconds": round(time.monotonic() - started, 3),
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
