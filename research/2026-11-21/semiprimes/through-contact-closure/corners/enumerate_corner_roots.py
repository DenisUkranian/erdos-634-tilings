#!/usr/bin/env python3
"""Exhaustive actual two-tile corner fans for unit F2 boards.

The existing unrestricted Geometry supplies complete endpoint placements.
No height, denominator, phase, odd-population, or spatial-search bound is
introduced. The separate verifier reconstructs the fans directly from their
two side-length orders and does not import this program or Geometry.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'research').is_dir() and
            (p / 'scripts').is_dir())
OLD = ROOT / 'research/2026-11-20/semiprimes/continuation'
sys.path.insert(0, str(OLD / 'global-endpoints/integer'))
sys.path.insert(0, str(OLD / 'vertex-phase'))
from global_core_sat import Geometry
from corner_oracle import CornerOracle

ANGLE = {'alpha': (1, 0), 'beta': (0, 1)}


def add(u, v):
    return u[0] + v[0], u[1] + v[1]


def sub(u, v):
    return u[0] - v[0], u[1] - v[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def scale(t, u):
    return t * u[0], t * u[1]


def physical(g, p):
    return Q(p[0], g.c ** p[2]), Q(p[1], g.c ** p[2])


def polygon(g, tile):
    return tuple(physical(g, p) for p in g.vertices(tile))


def positive_overlap(one, two):
    for left, right in ((one, two), (two, one)):
        for i, p in enumerate(left):
            edge = sub(left[(i + 1) % 3], p)
            if all(det(edge, sub(v, p)) <= 0 for v in right):
                return False
    return True


def rational_points(points):
    return [[str(x), str(y)] for x, y in points]


def wall_offsets(g, p):
    x, y = p
    result = []
    if y == 0:
        result.append(('OX', x, g.A))
    if g.B * x + g.A * y == g.A * g.B:
        result.append(('XY', Q(g.c * g.c) * y / g.B, g.c * g.c))
    if x == 0:
        result.append(('YO', g.B - y, g.B))
    return result


def placement_rejections(g, tile, index):
    result = []
    for k, p in enumerate(polygon(g, tile)):
        x, y = p
        if min(x, y, g.A * g.B - g.B * x - g.A * y) < 0:
            result.append({'kind': 'outside_board', 'tile': index, 'vertex': k})
            continue
        for wall, t, length in wall_offsets(g, p):
            if t.denominator != 1:
                result.append({'kind': 'nonintegral_boundary_offset',
                               'tile': index, 'vertex': k, 'wall': wall,
                               'offset': str(t)})
            elif not (g.coin[int(t)] and g.coin[length - int(t)]):
                result.append({'kind': 'boundary_prefix_semigroup',
                               'tile': index, 'vertex': k, 'wall': wall,
                               'offset': int(t)})
    return result


def boundary_gaps(g, triangles):
    intervals = {w: [] for w in ('OX', 'XY', 'YO')}
    lengths = dict(OX=g.A, XY=g.c * g.c, YO=g.B)
    for tri in triangles:
        for i, p in enumerate(tri):
            q = tri[(i + 1) % 3]
            first = {w: t for w, t, _ in wall_offsets(g, p)}
            second = {w: t for w, t, _ in wall_offsets(g, q)}
            for wall in first.keys() & second.keys():
                lo, hi = sorted((first[wall], second[wall]))
                if lo < hi:
                    intervals[wall].append((lo, hi))
    result, failures = [], []
    for wall, length in lengths.items():
        cursor = Q(0)
        gaps = []
        for lo, hi in sorted(intervals[wall]):
            if lo > cursor:
                gaps.append((cursor, lo))
            cursor = max(cursor, hi)
        if cursor < length:
            gaps.append((cursor, Q(length)))
        for lo, hi in gaps:
            delta = hi - lo
            good = delta.denominator == 1 and bool(g.coin[int(delta)])
            result.append({'wall': wall, 'from': str(lo), 'to': str(hi),
                           'length': str(delta), 'in_side_semigroup': good})
            if not good:
                failures.append({'kind': 'remaining_boundary_gap_semigroup',
                                 'wall': wall, 'from': str(lo), 'to': str(hi),
                                 'length': str(delta)})
    return result, failures


def outgoing(g, oracle, p, ray, angle):
    h, j = ray
    result = []
    # inverse is the proved complete 24-placement endpoint catalogue.
    for off, H, J, hand, _ in g.inverse(h, j % 3):
        tile = g.add(p, off), H, J, hand
        if oracle.sector(tile, p) != (ray, ANGLE[angle]):
            continue
        tri = g.vertices(tile)
        k = tri.index(p)
        vector = g.sub(tri[(k + 1) % 3], p)
        unit = g.unit(*ray)
        first_length = next(L for L in (g.a, g.b, g.c)
                            if vector == g.scale(L, unit))
        result.append((first_length, tile))
    result.sort()
    assert len(result) == 2 and result[0][0] < result[1][0]
    return result


def corner_variants(g):
    oracle = CornerOracle(g)
    specs = [
        ('O', (0, 0, 0), (0, 0), [('alpha', 'beta'), ('beta', 'alpha')]),
        ('X', (g.A, 0, 0), (2, 1), [('alpha', 'alpha')]),
        ('Y', (0, g.B, 0), (0, 4), [('beta', 'beta')]),
    ]
    all_variants = []
    for name, p, start, orders in specs:
        variants = []
        for angles in orders:
            seam_ray = oracle.advance(start, *ANGLE[angles[0]])
            for (L1, t1), (L2, t2) in product(
                    outgoing(g, oracle, p, start, angles[0]),
                    outgoing(g, oracle, p, seam_ray, angles[1])):
                first_other = next(L for L in (g.a, g.b, g.c)
                                   if L != L1 and
                                   {L, L1} == ({g.b, g.c} if angles[0] == 'alpha'
                                               else {g.a, g.c}))
                seam_lengths = [first_other, L2]
                variants.append({
                    'id': len(variants), 'corner': name, 'point': list(p),
                    'angles': list(angles), 'start_ray': list(start),
                    'first_side_lengths': [L1, L2],
                    'tiles': [t1, t2],
                    'vertices': [rational_points(polygon(g, t)) for t in (t1, t2)],
                    'seam': {'corner': name, 'origin': list(p),
                             'ray': list(seam_ray), 'incident_side_lengths': seam_lengths,
                             'guaranteed_length': max(seam_lengths),
                             'two_selected_banks_length': min(seam_lengths),
                             'unequal_side_lengths': seam_lengths[0] != seam_lengths[1]},
                })
        all_variants.append(variants)
    assert list(map(len, all_variants)) == [8, 4, 4]
    return all_variants


def seam_meetings(g):
    origins = [(Q(0), Q(0)), (Q(g.A), Q(0)), (Q(0), Q(g.B))]
    result = []
    for o_ray in ((-1, 1), (1, 0)):
        u = physical(g, g.unit(*o_ray))
        for k, ray in ((1, (1, 2)), (2, (1, 4))):
            v = physical(g, g.unit(*ray))
            displacement = sub(origins[k], origins[0])
            lam = det(displacement, v) / det(u, v)
            mu = det(displacement, u) / det(u, v)
            assert lam > 0 and mu > 0
            assert add(origins[0], scale(lam, u)) == add(origins[k], scale(mu, v))
            assert lam.denominator > 1 and mu.denominator > 1
            result.append({'O_ray': list(o_ray), 'other_corner': ('O', 'X', 'Y')[k],
                           'other_ray': list(ray), 'O_distance': str(lam),
                           'other_distance': str(mu),
                           'point': rational_points([scale(lam, u)])[0],
                           'forbid_both_initial_seams_reaching_meeting': True})
    return result


def enumerate_board(sides):
    g = Geometry(*sides)
    corners = corner_variants(g)
    meetings = seam_meetings(g)
    raw, surviving = [], []
    reject_counts = Counter()
    for variants in product(*corners):
        ids = [v['id'] for v in variants]
        name = 'O%d-X%d-Y%d' % tuple(ids)
        tiles = [t for v in variants for t in v['tiles']]
        triangles = [polygon(g, t) for t in tiles]
        reasons = [r for i, t in enumerate(tiles)
                   for r in placement_rejections(g, t, i)]
        for i, j in combinations(range(6), 2):
            if positive_overlap(triangles[i], triangles[j]):
                reasons.append({'kind': 'positive_area_overlap', 'tiles': [i, j]})
        gaps, bad_gaps = boundary_gaps(g, triangles)
        reasons.extend(bad_gaps)
        seams = [v['seam'] for v in variants]
        for meeting in meetings:
            if meeting['O_ray'] != seams[0]['ray']:
                continue
            other = 1 if meeting['other_corner'] == 'X' else 2
            if (seams[0]['guaranteed_length'] >= Q(meeting['O_distance']) and
                    seams[other]['guaranteed_length'] >= Q(meeting['other_distance'])):
                reasons.append({'kind': 'forbidden_corner_seam_meeting',
                                'other_corner': meeting['other_corner']})
        raw.append({'id': name, 'corner_variant_ids': ids,
                    'survives': not reasons, 'rejections': reasons})
        reject_counts.update(r['kind'] for r in reasons)
        if not reasons:
            surviving.append({'id': name, 'corner_variant_ids': ids,
                              'tiles': tiles, 'corner_tile_indices': [[0, 1], [2, 3], [4, 5]],
                              'seams': seams, 'remaining_boundary_gaps': gaps})
    assert len(raw) == 128
    control = None
    if g.N == 143:
        source = OLD / 'global-endpoints/tiling_143.json'
        actual = json.loads(source.read_text())
        keys = {json.dumps(t, separators=(',', ':')) for t in actual['tiles']}
        matches = [r['id'] for r in surviving
                   if all(json.dumps(t, separators=(',', ':')) in keys for t in r['tiles'])]
        assert len(matches) == 1
        control = {'source': str(source.relative_to(ROOT)),
                   'matching_surviving_root': matches[0],
                   'full_tiling_independently_checked_by': 'verify_corner_roots.py'}
    return {'schema': 'three-corner-roots-v1', 'sides': list(sides), 'N': g.N,
            'coordinate_convention': 'axial (x+y*rho)/c^e; rho^2=rho-1; tile=[q,h,j,s]',
            'board': [[0, 0, 0], [g.A, 0, 0], [0, g.B, 0]],
            'corner_variants': dict(zip(('O', 'X', 'Y'), corners)),
            'seam_constraints': meetings,
            'raw_root_count': len(raw), 'surviving_root_count': len(surviving),
            'rejection_counts': dict(sorted(reject_counts.items())),
            'raw_roots': raw, 'surviving_roots': surviving,
            'positive_control': control,
            'scope': 'Exhaustive necessary six-tile corner roots for unrestricted full tilings. Surviving roots are partial packings, not complete tilings or feasibility claims.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    reports = []
    for sides in ((33, 7, 37), (35, 13, 43), (5, 3, 7)):
        data = enumerate_board(sides)
        path = args.out / ('ROOTS_%d.json' % data['N'])
        path.write_text(json.dumps(data, indent=2) + '\n')
        reports.append({k: data[k] for k in ('N', 'raw_root_count', 'surviving_root_count',
                                           'rejection_counts', 'positive_control')})
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact checks require assertions.')
    main()
