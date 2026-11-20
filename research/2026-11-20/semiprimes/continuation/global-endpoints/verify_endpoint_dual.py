#!/usr/bin/env python3
"""Check a finite-support endpoint-current obstruction, using exact arithmetic.

No placement, orientation-height, coordinate-denominator, or phase bound is
imposed. See ENDPOINT_DUAL.md for the finite global pricing argument.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd, isqrt
from pathlib import Path


def rational(value):
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str):
        return Q(value)
    if isinstance(value, list) and len(value) == 2:
        return Q(value[0], value[1])
    raise ValueError("A rational must be an integer, a fraction string, or [n,d]; floats are rejected.")


def point(values):
    assert len(values) == 2
    return tuple(map(rational, values))


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def mul(p, q):
    return p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0] + p[1] * q[1]


def scale(t, p):
    return t * p[0], t * p[1]


def turn(p):
    return -p[1], p[0] + p[1]


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def norm(p):
    return p[0] * p[0] + p[0] * p[1] + p[1] * p[1]


def axis(p, q):
    x, y = sub(q, p)
    x, y = Q(x), Q(y)
    ix = x.numerator * y.denominator
    iy = y.numerator * x.denominator
    d = gcd(ix, iy)
    assert d > 0
    ix, iy = ix // d, iy // d
    return (ix, iy) if ix > 0 or (ix == 0 and iy > 0) else (-ix, -iy)


def unit_axis(values):
    """Normalize a rational axial direction whose squared norm is a square."""
    u = point(values)
    n = norm(u)
    assert n > 0
    numerator, denominator = isqrt(n.numerator), isqrt(n.denominator)
    assert numerator * numerator == n.numerator and denominator * denominator == n.denominator
    return scale(Q(denominator, numerator), u)


def ccw(polygon):
    polygon = tuple(polygon)
    area2 = sum(det(polygon[i], polygon[(i + 1) % len(polygon)]) for i in range(len(polygon)))
    assert area2 != 0
    return polygon if area2 > 0 else tuple(reversed(polygon))


def rows(polygon):
    polygon = ccw(polygon)
    result = Counter()
    for i, p in enumerate(polygon):
        q = polygon[(i + 1) % len(polygon)]
        ell = axis(p, q)
        result[p, ell] += 1
        result[q, ell] -= 1
    return {key: value for key, value in result.items() if value}


def render_point(p):
    return [str(p[0]), str(p[1])]


def strictly_inside(triangle, p):
    triangle = ccw(triangle)
    return all(det(sub(triangle[(i + 1) % 3], triangle[i]), sub(p, triangle[i])) > 0
               for i in range(3))


class Geometry:
    def __init__(self, sides, board, boundary_arithmetic=False):
        self.a, self.b, self.c = map(int, sides)
        a, b, c = self.a, self.b, self.c
        assert a > 0 and b > 0 and c > 0
        assert c * c == a * a + a * b + b * b
        self.board = ccw(board)
        assert len(self.board) == 3
        self.metric = sorted((a * a, b * b, c * c))
        self.boundary_arithmetic = boundary_arithmetic
        self.boundary_segments = []
        if boundary_arithmetic:
            for i, p in enumerate(self.board):
                q = self.board[(i + 1) % 3]
                n = norm(sub(q, p))
                assert n.denominator == 1
                length = isqrt(n.numerator)
                assert length * length == n.numerator
                self.boundary_segments.append((p, q, length))
            bound = max(length for _, _, length in self.boundary_segments)
            self.coins = [False] * (bound + 1)
            self.coins[0] = True
            for n in range(1, bound + 1):
                self.coins[n] = any(n >= side and self.coins[n - side] for side in (a, b, c))

    @lru_cache(None)
    def unit(self, height, phase):
        phase %= 6
        if height == 0:
            u = (Q(1), Q(0))
        elif height > 0:
            u = mul(self.unit(height - 1, 0), (Q(self.a, self.c), Q(self.b, self.c)))
        else:
            u = mul(self.unit(height + 1, 0), (Q(self.a + self.b, self.c), Q(-self.b, self.c)))
        for _ in range(phase):
            u = turn(u)
        assert norm(u) == 1
        return u

    def contained(self, p):
        return all(det(sub(self.board[(i + 1) % 3], self.board[i]), sub(p, self.board[i])) >= 0
                   for i in range(3))

    def admissible(self, triangle):
        if not all(self.contained(p) for p in triangle):
            return False
        if not self.boundary_arithmetic:
            return True
        for p in triangle:
            for left, right, length in self.boundary_segments:
                d, off = sub(right, left), sub(p, left)
                if det(d, off):
                    continue
                coordinate = 0 if d[0] else 1
                distance = off[coordinate] * length / d[coordinate]
                if distance.denominator != 1:
                    return False
                n = distance.numerator
                assert 0 <= n <= length
                if not self.coins[n] or not self.coins[length - n]:
                    return False
        return True

    def variants(self, p, height, phase):
        """All 24 placements with p an endpoint of an edge on the given axis."""
        u = self.unit(height, phase)
        yield from self.variants_by_unit(p, u)

    def variants_by_unit(self, p, u):
        assert norm(u) == 1
        orth = (-u[0] - 2 * u[1], 2 * u[0] + u[1])
        a, b, c = self.a, self.b, self.c
        for length, adjacent, last in ((a, b, c), (a, c, b), (b, a, c),
                                       (b, c, a), (c, a, b), (c, b, a)):
            projection = Q(length * length + adjacent * adjacent - last * last, 2 * length)
            altitude = Q(a * b, 2 * length)
            for direction in (-1, 1):
                q = add(p, scale(direction * length, u))
                for hand in (-1, 1):
                    r = add(p, add(scale(direction * projection, u), scale(hand * altitude, orth)))
                    triangle = tuple(sorted((p, q, r)))
                    assert sorted(norm(sub(triangle[i], triangle[(i + 1) % 3]))
                                  for i in range(3)) == self.metric
                    yield triangle


def verify(data):
    assert data.get("format", "endpoint-current-dual-v1") == "endpoint-current-dual-v1"
    boundary_arithmetic = data.get("boundary_arithmetic", False)
    assert isinstance(boundary_arithmetic, bool)
    geom = Geometry(data["sides"], [point(p) for p in data["board"]], boundary_arithmetic)
    weights = Counter()
    labels = {}
    for record in data["rows"]:
        if isinstance(record, dict):
            p = point(record["point"])
            if "axis" in record:
                u = unit_axis(record["axis"])
            else:
                height, phase = int(record["height"]), int(record["phase"])
                u = geom.unit(height, phase)
            value = rational(record["weight"])
        else:
            assert len(record) == 5
            x, y, height, phase, value = record
            p = point((x, y))
            height, phase, value = int(height), int(phase), rational(value)
            u = geom.unit(height, phase)
        key = (p, axis((0, 0), u))
        weights[key] += value
        labels[key] = u
    weights = {key: value for key, value in weights.items() if value}
    target = sum(value * weights.get(key, 0) for key, value in rows(geom.board).items())
    penalties = Counter()
    for record in data.get("point_penalties", []):
        if isinstance(record, dict):
            p, value = point(record["point"]), rational(record["weight"])
        else:
            assert len(record) == 3
            p, value = point(record[:2]), rational(record[2])
        assert value >= 0
        penalties[p] += value
    penalties = {p: value for p, value in penalties.items() if value}
    penalty_total = sum(penalties.values(), Q(0))
    adjusted_target = target - penalty_total
    board_area2 = sum(det(geom.board[i], geom.board[(i + 1) % 3]) for i in range(3))
    tile_count = Q(board_area2, geom.a * geom.b)
    candidates = set()
    for key in weights:
        p, _ = key
        if not geom.contained(p):
            continue
        for triangle in geom.variants_by_unit(p, labels[key]):
            if geom.admissible(triangle):
                candidates.add(triangle)
    positive = []
    maximum = Q(0)
    for triangle in sorted(candidates):
        score = sum(value * weights.get(key, 0) for key, value in rows(triangle).items())
        if score > 0 and penalties:
            xmin, xmax = min(p[0] for p in triangle), max(p[0] for p in triangle)
            ymin, ymax = min(p[1] for p in triangle), max(p[1] for p in triangle)
            for p, value in penalties.items():
                if xmin < p[0] < xmax and ymin < p[1] < ymax and strictly_inside(triangle, p):
                    score -= value
                    if score <= 0:
                        break  # Nonnegative remaining penalties cannot restore positivity.
        maximum = max(maximum, score)
        if score > 0:
            positive.append((score, triangle))
    positive.sort(reverse=True)
    integer_budget = tile_count.numerator // tile_count.denominator
    fractional_budget = tile_count - integer_budget
    budget_bound = sum((score for score, _ in positive[:integer_budget]), Q(0))
    if fractional_budget and integer_budget < len(positive):
        budget_bound += fractional_budget * positive[integer_budget][0]
    assert budget_bound <= tile_count * maximum
    margin = adjusted_target - budget_bound
    result = {
        "verified_global_nonexistence": margin > 0,
        "target": str(target),
        "point_penalty_total": str(penalty_total),
        "point_penalty_count": len(penalties),
        "adjusted_target_lower_bound": str(adjusted_target),
        "board_area_in_tile_units": str(tile_count),
        "global_obstruction_margin": str(margin),
        "uniform_score_obstruction_margin": str(adjusted_target - tile_count * maximum),
        "top_budget_score_bound": str(budget_bound),
        "boundary_arithmetic_used": boundary_arithmetic,
        "nonzero_support_rows": len(weights),
        "all_potentially_nonzero_contained_placements": len(candidates),
        "maximum_positive_column_score": str(maximum),
        "positive_scoring_placements": len(positive),
        "first_positive_scores": [
            {"score": str(score), "triangle": [render_point(p) for p in triangle]}
            for score, triangle in positive[:10]
        ],
    }
    return result


def self_test():
    # The exact 24-placement catalog has the right metric, both signs and hands.
    for sides in ((33, 7, 37), (35, 13, 43), (5, 3, 7)):
        a, b, c = sides
        big = ((-10000, -10000), (20000, -10000), (-10000, 20000))
        geom = Geometry(sides, big)
        for h, j in ((-2, 1), (0, 0), (3, 2)):
            p = (Q(17, 19), Q(-5, 11))
            variants = set(geom.variants(p, h, j))
            assert len(variants) == 24
            requested = (p, axis((0, 0), geom.unit(h, j)))
            assert all(requested in rows(t) for t in variants)

    # For a scale-two triangle the four true tile columns sum exactly to its
    # boundary, including the cancellation at subdivided straight segments.
    a, b, c = 33, 7, 37
    p, q, r = (Q(0), Q(0)), (Q(2 * a), Q(0)), (Q(2 * a), Q(2 * b))
    pq, pr, qr = scale(Q(1, 2), add(p, q)), scale(Q(1, 2), add(p, r)), scale(Q(1, 2), add(q, r))
    tiles = ((p, pq, pr), (pq, q, qr), (pr, qr, r), (pq, qr, pr))
    geom = Geometry((a, b, c), (p, q, r))
    total = Counter()
    for tile in tiles:
        assert sorted(norm(sub(tile[i], tile[(i + 1) % 3])) for i in range(3)) == geom.metric
        total.update(rows(tile))
    assert {key: value for key, value in total.items() if value} == rows((p, q, r))
    row_union = sorted({key for tile in tiles for key in rows(tile)})
    control = {
        "sides": [a, b, c],
        "board": [render_point(v) for v in (p, q, r)],
        "rows": [{"point": render_point(v), "axis": ell, "weight": (-1 if i % 2 else 1) * (i + 1)}
                 for i, (v, ell) in enumerate(row_union)],
    }
    result = verify(control)
    assert not result["verified_global_nonexistence"]
    assert Q(result["global_obstruction_margin"]) <= 0

    # A small similar target cannot contain a tile, so one positively weighted
    # target-corner row is a valid unrestricted obstruction.
    impossible = {
        "sides": [a, b, c],
        "board": [[0, 0], [str(Q(a, 2)), 0], [str(Q(a, 2)), str(Q(b, 2))]],
        "rows": [[0, 0, 0, 0, 1]],
    }
    result = verify(impossible)
    assert result["verified_global_nonexistence"]
    assert result["all_potentially_nonzero_contained_placements"] == 0

    # The same putative row certificate must fail on the original tile itself.
    possible = dict(impossible, board=[[0, 0], [a, 0], [a, b]])
    result = verify(possible)
    assert not result["verified_global_nonexistence"]
    assert result["positive_scoring_placements"] >= 1
    assert result["global_obstruction_margin"] == "0"

    # Interior penalties lower both the single real tile's score and the
    # target lower bound equally. A point on its edge must not be penalized.
    penalized = dict(possible, rows=[[0, 0, 0, 0, 2]], point_penalties=[
        {"point": [str(Q(2 * a, 3)), str(Q(b, 3))], "weight": 1}
    ])
    result = verify(penalized)
    assert not result["verified_global_nonexistence"]
    assert result["global_obstruction_margin"] == "0"
    assert result["maximum_positive_column_score"] == "1"
    edge_penalized = dict(penalized, point_penalties=[{"point": [str(Q(a, 2)), 0], "weight": 1}])
    result = verify(edge_penalized)
    assert not result["verified_global_nonexistence"]
    assert result["maximum_positive_column_score"] == "2"
    assert result["global_obstruction_margin"] == "-1"

    # A half-integral contact with the exterior is geometrically contained but
    # cannot occur in a tiling whose boundary edges all have integer lengths.
    board = tuple(map(point, ((0, 0), (1000, 0), (0, 1000))))
    loose, strict = Geometry((a, b, c), board), Geometry((a, b, c), board, True)
    shifted = tuple(add((Q(1, 2), Q(0)), p) for p in map(point, ((0, 0), (a, 0), (a, b))))
    assert loose.admissible(shifted)
    assert not strict.admissible(shifted)
    print("Exact catalog, subdivision, negative control, and positive control checks passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    if args.self_test:
        self_test()
    if args.certificate:
        result = verify(json.loads(args.certificate.read_text()))
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result["verified_global_nonexistence"] else 2)
    if not args.self_test:
        parser.error("Provide a certificate or --self-test.")


if __name__ == "__main__":
    main()
