#!/usr/bin/env python3
"""Independent standard-library replay of all unrestricted corner roots.

This verifier imports neither the enumerator, Geometry, nor CornerOracle.
It constructs corner triangles directly from the two adjacent-side orders,
checks actual rational coordinates, and verifies the complete 143 tiling
by containment, area, and every pairwise separating-axis test.
"""
from fractions import Fraction as Q
from heapq import heappop, heappush
from itertools import combinations, product
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'research').is_dir() and
            (p / 'scripts').is_dir())
U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def times(k, p):
    return k * p[0], k * p[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def mul(p, q):
    return p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0] + p[1] * q[1]


def norm(p):
    return p[0] * p[0] + p[0] * p[1] + p[1] * p[1]


def power(z, h):
    if h < 0:
        z = (z[0] + z[1], -z[1])
        h = -h
    answer = (Q(1), Q(0))
    while h:
        if h & 1:
            answer = mul(answer, z)
        z = mul(z, z)
        h //= 2
    return answer


def ccw(poly):
    return tuple(poly) if cross(sub(poly[1], poly[0]), sub(poly[2], poly[0])) > 0 else tuple(reversed(poly))


def canonical(poly):
    return tuple(sorted(poly))


def separated(p, q):
    for first, second in ((p, q), (q, p)):
        for i, start in enumerate(first):
            direction = sub(first[(i + 1) % 3], start)
            if max(cross(direction, sub(v, start)) for v in second) <= 0:
                return True
    return False


def decode_tile(sides, item):
    a, b, c = sides
    q0, h, j, hand = item
    assert all(type(n) is int for n in [*q0, h, j, hand])
    x, y, e = q0
    assert e >= 0 and 0 <= j < 6 and hand in (-1, 1)
    q = Q(x, c ** e), Q(y, c ** e)
    z = Q(a, c), Q(b, c)
    first = mul(power(z, h), U[j])
    second = mul(power(z, h), U[(j + hand) % 6])
    poly = ccw((add(q, times(-a, first)), q, add(q, times(b, second))))
    assert sorted(norm(sub(poly[(i + 1) % 3], poly[i])) for i in range(3)) == sorted((a*a, b*b, c*c))
    assert cross(sub(poly[1], poly[0]), sub(poly[2], poly[0])) == a * b
    return poly


def membership_oracle(a, b, c):
    # Independent semigroup algorithm: shortest distances modulo b.
    distances = [10**30] * b
    distances[0] = 0
    queue = [(0, 0)]
    while queue:
        value, residue = heappop(queue)
        if value != distances[residue]:
            continue
        for length in (a, c):
            new = value + length
            r = new % b
            if new < distances[r]:
                distances[r] = new
                heappush(queue, (new, r))
    return lambda n: Q(n).denominator == 1 and n >= 0 and n >= distances[int(n) % b]


def wall_data(p, A, B, c):
    x, y = p
    answer = {}
    if y == 0:
        answer['OX'] = x
    if B * x + A * y == A * B:
        answer['XY'] = Q(c*c) * y / B
    if x == 0:
        answer['YO'] = B - y
    return answer


def check_placement(poly, sides, coin):
    a, b, c = sides
    A, B = b * (2*a+b), a * (a+2*b)
    lengths = {'OX': A, 'XY': c*c, 'YO': B}
    for p in poly:
        x, y = p
        assert x >= 0 and y >= 0 and B*x+A*y <= A*B
        for wall, offset in wall_data(p, A, B, c).items():
            assert coin(offset) and coin(lengths[wall]-offset)


def direct_fans(sides):
    a, b, c = sides
    A, B = b * (2*a+b), a * (a+2*b)
    z = Q(a, c), Q(b, c)
    rho = (Q(0), Q(1))
    rotations = {'alpha': mul(rho, (z[0]+z[1], -z[1])), 'beta': z}
    lengths = {'alpha': ((b, c), (c, b)), 'beta': ((a, c), (c, a))}
    specs = [
        ('O', (Q(0), Q(0)), (Q(1), Q(0)), [('alpha','beta'),('beta','alpha')]),
        ('X', (Q(A), Q(0)), (Q(-A, c*c), Q(B, c*c)), [('alpha','alpha')]),
        ('Y', (Q(0), Q(B)), (Q(0), Q(-1)), [('beta','beta')]),
    ]
    result = {}
    for name, p, start, orders in specs:
        fans = []
        for angles in orders:
            middle = mul(start, rotations[angles[0]])
            end = mul(middle, rotations[angles[1]])
            for (l1, r1), (l2, r2) in product(lengths[angles[0]], lengths[angles[1]]):
                first = (p, add(p, times(l1, start)), add(p, times(r1, middle)))
                second = (p, add(p, times(l2, middle)), add(p, times(r2, end)))
                assert cross(sub(first[1], p), sub(first[2], p)) == a*b
                assert cross(sub(second[1], p), sub(second[2], p)) == a*b
                fans.append({'polygons': (first, second), 'angles': list(angles),
                             'first_side_lengths': [l1, l2],
                             'seam_lengths': [r1, l2], 'seam_unit': middle,
                             'point': p})
        result[name] = fans
    return result


def gap_records(polys, sides, coin):
    a, b, c = sides
    A, B = b * (2*a+b), a * (a+2*b)
    lengths = {'OX': A, 'XY': c*c, 'YO': B}
    occupied = {w: [] for w in lengths}
    for poly in polys:
        for i, p in enumerate(poly):
            q = poly[(i+1) % 3]
            left, right = wall_data(p, A, B, c), wall_data(q, A, B, c)
            for wall in left.keys() & right.keys():
                lo, hi = min(left[wall], right[wall]), max(left[wall], right[wall])
                if lo != hi:
                    occupied[wall].append((lo, hi))
    answer = []
    for wall, length in lengths.items():
        covered_until = Q(0)
        for lo, hi in sorted(occupied[wall]) + [(Q(length), Q(length))]:
            if lo > covered_until:
                assert coin(lo-covered_until)
                answer.append({'wall': wall, 'from': str(covered_until), 'to': str(lo),
                               'length': str(lo-covered_until), 'in_side_semigroup': True})
            covered_until = max(covered_until, hi)
    return answer


def check_seams(data, sides):
    a, b, c = sides
    A, B = b*(2*a+b), a*(a+2*b)
    z = Q(a, c), Q(b, c)
    p, q = a+2*b, 2*a+b
    expected = {
        ((1,0),'X'): (Q(a*b*q,c), Q(b*b*q,c)),
        ((1,0),'Y'): (Q(a*b*p,c), Q(a*a*p,c)),
        ((-1,1),'X'): (Q(b*c*q,p), Q(b*c*q,p)),
        ((-1,1),'Y'): (Q(a*c*p,q), Q(a*c*p,q)),
    }
    actual = {}
    for entry in data['seam_constraints']:
        key = tuple(entry['O_ray']), entry['other_corner']
        lam, mu = Q(entry['O_distance']), Q(entry['other_distance'])
        assert (lam, mu) == expected[key]
        assert lam.denominator > 1 and mu.denominator > 1
        assert lam > c and mu > c
        u = mul(power(z, entry['O_ray'][0]), U[entry['O_ray'][1]])
        v = mul(power(z, entry['other_ray'][0]), U[entry['other_ray'][1]])
        origin = (Q(A), Q(0)) if key[1] == 'X' else (Q(0), Q(B))
        meeting = times(lam, u)
        assert meeting == add(origin, times(mu, v))
        assert [str(t) for t in meeting] == entry['point']
        assert entry['forbid_both_initial_seams_reaching_meeting'] is True
        actual[key] = (lam, mu)
    assert actual == expected
    return {'forbidden_seam_pair_thresholds_checked': 4,
            'additional_root_exclusions': 0,
            'all_meeting_distances_exceed_largest_corner_side': True}


def check_roots(path):
    data = json.loads(path.read_text())
    assert data['schema'] == 'three-corner-roots-v1'
    sides = tuple(data['sides'])
    a, b, c = sides
    assert sides in ((33,7,37),(35,13,43),(5,3,7))
    assert c*c == a*a+a*b+b*b
    A, B = b*(2*a+b), a*(a+2*b)
    assert data['N'] == (a+2*b)*(2*a+b)
    assert data['board'] == [[0,0,0],[A,0,0],[0,B,0]]
    coin = membership_oracle(*sides)
    fans = direct_fans(sides)
    assert [len(fans[name]) for name in ('O','X','Y')] == [8,4,4]
    decoded = {}
    unequal = 0
    for name in ('O','X','Y'):
        stored = data['corner_variants'][name]
        assert len(stored) == len(fans[name])
        decoded[name] = []
        for index, (expected, actual) in enumerate(zip(fans[name], stored)):
            assert actual['id'] == index and actual['corner'] == name
            assert actual['angles'] == expected['angles']
            assert actual['first_side_lengths'] == expected['first_side_lengths']
            polys = tuple(decode_tile(sides, t) for t in actual['tiles'])
            assert [canonical(p) for p in polys] == [canonical(p) for p in expected['polygons']]
            assert actual['vertices'] == [[[str(x),str(y)] for x,y in p] for p in polys]
            for poly in polys:
                check_placement(poly, sides, coin)
            assert separated(*polys)
            seam = actual['seam']
            assert seam['incident_side_lengths'] == expected['seam_lengths']
            assert seam['guaranteed_length'] == max(expected['seam_lengths'])
            assert seam['two_selected_banks_length'] == min(expected['seam_lengths'])
            assert seam['unequal_side_lengths'] == (expected['seam_lengths'][0] != expected['seam_lengths'][1])
            z = Q(a,c), Q(b,c)
            assert mul(power(z,seam['ray'][0]),U[seam['ray'][1]]) == expected['seam_unit']
            assert max(expected['seam_lengths']) <= c
            unequal += seam['unequal_side_lengths']
            decoded[name].append(polys)
    roots = {r['id']: r for r in data['surviving_roots']}
    raw = {r['id']: r for r in data['raw_roots']}
    assert len(roots) == len(raw) == 128
    assert data['raw_root_count'] == data['surviving_root_count'] == 128
    assert data['rejection_counts'] == {}
    root_sets = {}
    total_pair_checks = 0
    for ids in product(range(8), range(4), range(4)):
        name = 'O%d-X%d-Y%d' % ids
        root, raw_item = roots[name], raw[name]
        assert raw_item == {'id':name,'corner_variant_ids':list(ids),'survives':True,'rejections':[]}
        assert root['corner_variant_ids'] == list(ids)
        assert root['corner_tile_indices'] == [[0,1],[2,3],[4,5]]
        variants = [data['corner_variants'][cname][i] for cname,i in zip(('O','X','Y'),ids)]
        assert root['tiles'] == [t for v in variants for t in v['tiles']]
        assert root['seams'] == [v['seam'] for v in variants]
        polys = tuple(p for cname,index in zip(('O','X','Y'),ids) for p in decoded[cname][index])
        assert len({canonical(p) for p in polys}) == 6
        for first, second in combinations(polys,2):
            assert separated(first,second)
            total_pair_checks += 1
        assert root['remaining_boundary_gaps'] == gap_records(polys,sides,coin)
        root_sets[name] = frozenset(canonical(p) for p in polys)
    assert len(set(root_sets.values())) == 128
    report = {'N':data['N'], 'raw_patterns':128, 'surviving_patterns':128,
              'distinct_physical_roots':128, 'independent_corner_variants':16,
              'unequal_seam_variants_retained':unequal,
              'root_triangle_pair_checks':total_pair_checks,
              'boundary_semigroup_check':'Independent shortest-residue algorithm',
              'height_or_odd_population_cutoff':False,
              'seam_constraints':check_seams(data,sides)}
    if data['N'] == 143:
        source = ROOT / data['positive_control']['source']
        known = json.loads(source.read_text())
        assert known['sides'] == [5,3,7] and known['N'] == 143
        polys = [decode_tile(sides,t) for t in known['tiles']]
        assert len(polys) == len({canonical(p) for p in polys}) == 143
        for poly in polys:
            check_placement(poly,sides,coin)
        for first,second in combinations(polys,2):
            assert separated(first,second)
        assert sum(cross(sub(p[1],p[0]),sub(p[2],p[0])) for p in polys) == A*B
        corners = ((Q(0),Q(0)),(Q(A),Q(0)),(Q(0),Q(B)))
        at_corners = [[p for p in polys if vertex in p] for vertex in corners]
        assert [len(v) for v in at_corners] == [2,2,2]
        actual_set = frozenset(canonical(p) for group in at_corners for p in group)
        matches = [name for name,pattern in root_sets.items() if pattern == actual_set]
        assert matches == [data['positive_control']['matching_surviving_root']]
        report['positive_143_control'] = {
            'whole_tiling_checked':True, 'pairwise_interior_disjointness_checks':143*142//2,
            'area_and_containment_checked':True,
            'corner_tile_counts':[2,2,2], 'surviving_root':matches[0]}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=HERE)
    parser.add_argument('--out',type=Path,default=HERE/'CORNER_ROOT_REPLAY.json')
    args = parser.parse_args()
    report = {'status':'PASS',
              'boards':[check_roots(args.directory/('ROOTS_%d.json'%N)) for N in (3431,5063,143)],
              'scope':'Complete necessary corner-root enumeration only. No full target exclusion or completion is asserted.'}
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact checks require assertions.')
    main()
