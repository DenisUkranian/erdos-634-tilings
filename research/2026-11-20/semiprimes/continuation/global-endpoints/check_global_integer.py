#!/usr/bin/env python3
"""Independent exact geometry/encoding controls for the global integer model."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import random
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


engine = load('global_integer_audit_target', ROOT / 'integer/global_core_sat.py')
independent = load('independent_metric', ROOT / 'verify_endpoint_dual.py')
pointcuts = load('independent_overlap', ROOT / 'lp/point_coverage.py')


def rational_point(g, p):
    return Q(p[0], g.c ** p[2]), Q(p[1], g.c ** p[2])


def shape(g, key):
    return tuple(sorted(rational_point(g, p) for p in g.vertices(key)))


class Powers:
    def __init__(self, c):
        self.c = c

    def __getitem__(self, exponent):
        return self.c ** exponent


def catalogue_controls():
    rng = random.Random(634)
    checked, wedges = 0, 0
    for sides in ((5, 3, 7), (33, 7, 37), (35, 13, 43)):
        g = engine.Geometry(*sides)
        metric = independent.Geometry(sides, ((0, 0), (g.A, 0), (0, g.B)), True)
        overlap = pointcuts.ExactGeometry(g.c, g.template, g.add, Powers(g.c))
        points = []
        for w, (_, _, h, j) in enumerate(g.walls()):
            all_points = list(g.wall_points(w))
            sample = all_points if sides == (5, 3, 7) else rng.sample(all_points, min(25, len(all_points)))
            points.extend((p, h, j) for _, p in sample)
        points.extend(((g.A // 3, g.B // 3, 0), h, j)
                      for h in (-3, 0, 4) for j in range(3))
        for row in points:
            p, h, j = row
            p = rational_point(g, p)
            expected = {t for t in metric.variants(p, h, j) if metric.admissible(t)}
            candidates = list(g.incident(row))
            actual = {shape(g, key) for key, _ in candidates}
            assert actual == expected, (sides, row, len(actual), len(expected))
            checked += 1
            groups = defaultdict(list)
            for key, coefficient in candidates:
                polygon_rows = independent.rows(shape(g, key))
                actual_rows = Counter()
                for (point, hh, jj), value in g.rows(key):
                    axis = independent.axis((0, 0), metric.unit(hh, jj))
                    actual_rows[rational_point(g, point), axis] -= value
                assert dict(actual_rows) == polygon_rows
                groups[g.wedge(key, row)].append(key)
            if row[0] == (g.A // 3, g.B // 3, 0):
                for group in groups.values():
                    for one, two in combinations(group, 2):
                        assert overlap.overlap_point(one, two) is not None
                        wedges += 1
    return checked, wedges


def positive_control():
    data = json.loads((ROOT / 'tiling_143.json').read_text())
    g = engine.Geometry(*data['sides'])
    metric = independent.Geometry(data['sides'], ((0, 0), (g.A, 0), (0, g.B)), True)
    keys = [(tuple(q), h, j, s) for q, h, j, s in data['tiles']]
    triangles = [shape(g, key) for key in keys]
    assert len(keys) == g.N == len(set(triangles)) == 143
    current = Counter()
    area = Q(0)
    for triangle in triangles:
        assert metric.admissible(triangle)
        lengths = sorted(independent.norm(independent.sub(triangle[i], triangle[(i + 1) % 3]))
                         for i in range(3))
        assert lengths == [9, 25, 49]
        ccw = independent.ccw(triangle)
        area += sum(independent.det(ccw[i], ccw[(i + 1) % 3]) for i in range(3))
        current.update(independent.rows(triangle))
    current.subtract(independent.rows(metric.board))
    assert not any(current.values())
    assert area == g.A * g.B == g.N * g.a * g.b
    # Check every exterior unit interval directly from actual geometric edges.
    for w, (left, right, _, _) in enumerate(g.walls()):
        L = (g.A, g.c * g.c, g.B)[w]
        offsets = dict(g.wall_points(w))
        locations = {rational_point(g, p): k for k, p in offsets.items()}
        coverage = [0] * L
        for triangle in triangles:
            endpoint = [locations[p] for p in triangle if p in locations]
            if len(endpoint) == 2:
                lo, hi = sorted(endpoint)
                for k in range(lo, hi):
                    coverage[k] += 1
        assert coverage == [1] * L
    # An additional metric test independent of endpoint cancellation.
    overlap = pointcuts.ExactGeometry(g.c, g.template, g.add, Powers(g.c))
    pair_count = 0
    for one, two in combinations(keys, 2):
        _, d1, _, b1 = overlap.geometry(one)
        _, d2, _, b2 = overlap.geometry(two)
        if b1[1] * d2 <= b2[0] * d1 or b2[1] * d1 <= b1[0] * d2:
            continue
        if b1[3] * d2 <= b2[2] * d1 or b2[3] * d1 <= b1[2] * d2:
            continue
        assert overlap.overlap_point(one, two) is None
        pair_count += 1
    return pair_count


def pseudo_boolean_controls():
    smt = engine.SMT()
    commands, expected = [], []
    for n in range(5):
        for bits in product((False, True), repeat=n):
            terms = ['true' if x else 'false' for x in bits]
            for bound in range(-1, n + 2):
                commands.append('(simplify ' + engine.equal(bound, terms) + ')')
                expected.append('true' if sum(bits) == bound else 'false')
                commands.append('(simplify ' + engine.atmost(bound, terms) + ')')
                expected.append('true' if sum(bits) <= bound else 'false')
    actual = smt.run('\n'.join(commands)).splitlines()
    assert actual == expected, next((i, x, y) for i, (x, y) in enumerate(zip(actual, expected)) if x != y)
    return len(expected)


def shared_guard_and_rebuild_control():
    """Exercise changing shared guards and a rebuild with pending new input."""
    with tempfile.TemporaryDirectory(prefix='guard-audit-') as out:
        args = SimpleNamespace(sides=(5, 3, 7), out=out, random_seed=634,
                               point_checkpoint=None, proof=False,
                               timeout_ms=3000, minimize_core=False)
        search = engine.Search(args)
        one = ((1, 1, 0), 0, 0)
        two = ((2, 1, 0), 0, 0)
        event = {0: [(one, 1), (two, -1)],
                 1: [(one, -1), (two, 1)], 2: [(one, 1)]}
        search.g.rows = lambda tile: event[tile]
        search.insert(0)
        search.insert(1)
        search.update_guards(0)
        assert len(search.guard_rows) == 1
        shared = search.guards[one]
        assert search.guards[two] == shared
        assert set(search.guard_rows[shared]) == {one, two}
        search.flush()
        assert search.smt.run('(push 1)\n(assert (not (= x0 x1)))\n(check-sat-assuming (' + shared + '))') == 'unsat'
        assert search.smt.run('(check-sat)') == 'sat'
        assert search.smt.run('(pop 1)') == ''
        search.insert(2)
        search.update_guards(2)
        newest = search.guards[one]
        assert newest != shared
        assert search.guard_rows[shared] == [two]
        search.unbind(two)
        assert set(search.guard_rows) == {newest}
        search.assert_('x2')
        # x2's declaration, new guard, and permanent clause are still pending.
        search.rebuild(1)
        search.flush()
        assert set(search.guard_clauses) == {newest}
        assert search.smt.run('(check-sat-assuming (' + newest + '))') == 'sat'
        values = search.smt.run('(get-value (x0 x1 x2))')
        assert '(x0 false)' in values and '(x1 true)' in values and '(x2 true)' in values
        search.journal.close()
        search.smt.close()
    return True


if __name__ == '__main__':
    rows, wedges = catalogue_controls()
    pairs = positive_control()
    encodings = pseudo_boolean_controls()
    guards = shared_guard_and_rebuild_control()
    print(json.dumps(dict(metric_catalogues=rows, same_wedge_positive_overlaps=wedges,
                          positive_control_tiles=143, positive_control_intersection_checks=pairs,
                          pseudo_boolean_truth_cases=encodings,
                          shared_guard_rebuild_control=guards), indent=2))
